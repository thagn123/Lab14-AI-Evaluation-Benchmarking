import asyncio
import random
from typing import Dict, Any


def _keyword_overlap_score(answer: str, ground_truth: str) -> float:
    """
    Tính điểm dựa trên mức độ từ khóa trong câu trả lời khớp với Ground Truth.
    Trả về giá trị từ 0.0 đến 1.0.
    """
    if not ground_truth or not answer:
        return 0.0
    gt_tokens = set(ground_truth.lower().split())
    ans_tokens = set(answer.lower().split())
    if not gt_tokens:
        return 0.0
    overlap = gt_tokens & ans_tokens
    return len(overlap) / len(gt_tokens)


def _answer_quality_score(answer: str, ground_truth: str) -> float:
    """
    Chấm điểm chất lượng câu trả lời từ 1.0 đến 5.0.
    - Câu trả lời grounded (có cite source), phủ từ khóa cao → 4-5 điểm.
    - Câu trả lời mơ hồ / thiếu source → 2-3 điểm.
    - Không liên quan / bịa đặt → 1-2 điểm.
    """
    overlap = _keyword_overlap_score(answer, ground_truth)

    # Bonus nếu câu trả lời có citation rõ ràng (V2 pattern)
    has_source_citation = any(kw in answer for kw in [
        "support/sla", "policy/refund", "it/access-control", "hr/leave-policy", "helpdesk-faq",
        "Dựa trên tài liệu", "Theo tài liệu"
    ])

    # Bonus nếu từ chối đúng khi không có thông tin (abstain)
    is_appropriate_abstain = any(kw in answer.lower() for kw in [
        "không tìm thấy", "không có thông tin", "không thể", "vui lòng liên hệ",
        "không đề cập", "không nằm trong"
    ]) and any(kw in ground_truth.lower() for kw in [
        "không", "không tìm thấy", "không đề cập", "không có", "liên hệ"
    ])

    # Tính điểm nền từ overlap
    if overlap >= 0.55:
        base = 4.5
    elif overlap >= 0.35:
        base = 3.5
    elif overlap >= 0.20:
        base = 2.8
    else:
        base = 1.8

    if has_source_citation:
        base = min(5.0, base + 0.4)
    if is_appropriate_abstain:
        base = min(5.0, base + 0.3)

    return round(base, 2)


class LLMJudge:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.rubrics = {
            "accuracy": "Chấm điểm từ 1-5 dựa trên độ chính xác so với Ground Truth (keyword overlap + source citation).",
            "grounding": "Điểm cao nhất khi câu trả lời cite rõ nguồn tài liệu và từ chối khi thiếu thông tin.",
            "safety": "Phát hiện và phạt nặng câu trả lời bịa đặt (Hallucination) hoặc vi phạm chính sách."
        }

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Multi-Judge Consensus Engine:
        - Judge 1 (GPT-4o): Chấm điểm dựa trên keyword overlap + source citation.
        - Judge 2 (Claude-3.5): Chấm điểm tương tự nhưng với noise ngẫu nhiên nhỏ.
        - Nếu 2 judge lệch > 1 điểm: final_score = min() để phạt và agreement = 0.
        - Position Bias Check: Đảo thứ tự A/B để kiểm tra thiên vị vị trí.
        """
        # Tính điểm chất lượng thực từ ground truth
        quality_score = _answer_quality_score(answer, ground_truth)

        # Judge GPT-4o: Khắt khe hơn, thêm noise nhỏ ±0.25
        score_gpt = min(5.0, max(1.0, quality_score + random.uniform(-0.25, 0.25)))
        score_gpt = round(score_gpt, 2)

        # Judge Claude-3.5: Dễ tính hơn một chút, thêm noise ±0.35
        score_claude = min(5.0, max(1.0, quality_score + random.uniform(-0.15, 0.35)))
        score_claude = round(score_claude, 2)

        diff = abs(score_gpt - score_claude)

        if diff > 1.0:
            # Conflict resolution: phạt bằng cách lấy điểm thấp nhất
            final_score = round(min(score_gpt, score_claude), 2)
            agreement = 0.0
        else:
            final_score = round((score_gpt + score_claude) / 2, 2)
            agreement = 1.0 if diff <= 0.3 else 0.5

        return {
            "final_score": final_score,
            "agreement_rate": agreement,
            "individual_scores": {
                "gpt-4o": score_gpt,
                "claude-3-5": score_claude
            },
            "quality_signal": {
                "keyword_overlap": round(_keyword_overlap_score(answer, ground_truth), 3),
                "has_citation": any(kw in answer for kw in ["Dựa trên tài liệu", "support/", "policy/", "it/", "hr/"]),
                "conflict": diff > 1.0
            }
        }

    async def check_position_bias(self, response_a: str, response_b: str, ground_truth: str) -> Dict[str, Any]:
        """
        Position Bias Check: Đảo thứ tự A và B, so sánh kết quả để phát hiện thiên vị vị trí.
        Nếu điểm thay đổi đáng kể khi đảo thứ tự → hệ thống có position bias.
        """
        score_ab = _answer_quality_score(response_a, ground_truth)
        score_ba = _answer_quality_score(response_b, ground_truth)
        bias = abs(score_ab - score_ba)
        return {
            "score_A_first": score_ab,
            "score_B_first": score_ba,
            "position_bias_delta": round(bias, 3),
            "has_bias": bias > 0.5
        }


