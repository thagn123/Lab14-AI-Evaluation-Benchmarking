# AI Evaluation Factory Workflow

Dưới đây là sơ đồ kiến trúc và luồng xử lý (workflow) của hệ thống tự động đánh giá mà chúng ta đã xây dựng trong dự án Lab 14:

```mermaid
graph TD
    %% Define styles
    classDef dataFill fill:#e0f7fa,stroke:#006064,stroke-width:2px;
    classDef agentFill fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef evalFill fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef gateFill fill:#fce4ec,stroke:#880e4f,stroke-width:2px;

    %% Data Source
    subgraph Data Generation
        A[synthetic_gen.py] -->|Generate| B(Golden Dataset jsonl)
        B -.-> |50+ Cases: Standard, Adversarial, Edge| C
    end
    class A,B dataFill

    %% Runner & Agents
    subgraph Async Benchmark Runner
        C[runner.py - Async Batch Processing]
        
        C -->|Test Query| D(MainAgent V1)
        C -->|Test Query| E(MainAgent V2 Optimized)
        
        D -->|Response & Retrieved Context| F[Evaluation Pipeline]
        E -->|Response & Retrieved Context| F
    end
    class C,D,E agentFill

    %% Evaluation Engine
    subgraph Evaluation Pipeline
        F --> G{Retrieval Evaluator}
        F --> H{Multi-Model LLM Judge}
        
        G -->|Hit Rate| I[RAGAS Metrics]
        G -->|MRR| I
        
        H -->|Claude 3.5| J[Score A]
        H -->|GPT-4o| K[Score B]
        J --> L((Consensus Logic))
        K --> L((Consensus Logic))
        L -->|Calculate Agreement Rate| M[Final Judge Score]
        L -->|Penalty if Delta > 1| M
    end
    class F,G,H,I,J,K,L,M evalFill

    %% CI/CD Gate
    subgraph Release Regression Gate
        N[main.py]
        I --> N
        M --> N
        
        N -->|Compare Average Score V1 vs V2| O{Decision Gate}
        O -->|Delta > 0| P((APPROVE: Release V2))
        O -->|Delta <= 0| Q((BLOCK: Rollback to V1))
        
        P --> R[summary.json & benchmark_results.json]
        Q --> R
    end
    class N,O,P,Q,R gateFill
```

### Giải thích quy trình xử lý:
1. **Bước 1 (Data Generation):** Sinh tự động tập dữ liệu `golden_set` gồm 50 cases đa dạng.
2. **Bước 2 (Async Processing):** Chạy song song hàng loạt test cases trên cả cụm Agent V1 và V2 nhằm tiết kiệm thời gian và tránh timeouts.
3. **Bước 3 (Evaluation):**
   - **RAG Retrieval:** Công cụ đánh giá Hit Rate và MRR để xác nhận Vector DB có bốc được đúng đoạn văn bản cần tìm không.
   - **Multi-Judge consensus:** Cả mô hình GPT-4o và Claude 3.5 đều chấm điểm độc lập. Nút Consensus (đồng thuận) sẽ tính điểm theo trung bình chung, đồng thời phạt nặng nếu hai kết quả lệch xa nhau.
4. **Bước 4 (Gate Check):** So sánh hiệu năng của bản cập nhật (V2) với bản hiện tại (V1). Nếu chất lượng tăng (*Delta > 0*), hệ thống cấp phép Deploy và xuất report.
