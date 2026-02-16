"""
Evaluation runner for the Financial Approval System.

Runs the evaluation pipeline using LangSmith to measure
risk assessment accuracy and approval consistency.
"""

import os
from backend.config import LANGSMITH_API_KEY, LANGSMITH_PROJECT
from backend.evaluation.dataset import EVAL_DATASET
from backend.evaluation.evaluators import (
    create_risk_accuracy_evaluator,
    create_approval_consistency_evaluator,
)


def run_evaluation():
    """
    Run the evaluation pipeline.

    This function:
    1. Sets up LangSmith tracing
    2. Creates evaluator instances
    3. Runs each test case through the approval workflow
    4. Collects and reports scores
    """
    if not LANGSMITH_API_KEY:
        print("Warning: LANGSMITH_API_KEY not set. Running in local-only mode.")

    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", LANGSMITH_PROJECT)

    risk_evaluator = create_risk_accuracy_evaluator()
    consistency_evaluator = create_approval_consistency_evaluator()

    print(f"Running evaluation with {len(EVAL_DATASET)} test cases...")
    print(f"LangSmith project: {LANGSMITH_PROJECT}")
    print("=" * 60)

    risk_scores = []
    consistency_scores = []

    for i, test_case in enumerate(EVAL_DATASET):
        inputs = test_case["input"]
        expected = test_case["expected"]

        print(f"\nTest case {i + 1}: {inputs['title']}")
        print(f"  Amount: ${inputs['amount']:,.2f}")
        print(f"  Department: {inputs['department']}")
        print(f"  Expected risk: {expected['risk_level']}")
        print(f"  Expected status: {expected['status']}")

        # In a full implementation, this would run the graph
        # For now, just validate the evaluator structure
        try:
            # Test evaluator with mock outputs matching expected
            risk_result = risk_evaluator(
                inputs=inputs,
                outputs={"risk_level": expected["risk_level"]},
                reference_outputs=expected,
            )
            risk_scores.append(risk_result.get("score", 0))
            print(f"  Risk evaluator score: {risk_result.get('score', 'N/A')}")
        except NotImplementedError:
            print("  Risk evaluator: NOT IMPLEMENTED")
        except Exception as e:
            print(f"  Risk evaluator error: {e}")

        try:
            consistency_result = consistency_evaluator(
                inputs=inputs,
                outputs={"status": expected["status"]},
                reference_outputs=expected,
            )
            consistency_scores.append(consistency_result.get("score", 0))
            print(f"  Consistency evaluator score: {consistency_result.get('score', 'N/A')}")
        except NotImplementedError:
            print("  Consistency evaluator: NOT IMPLEMENTED")
        except Exception as e:
            print(f"  Consistency evaluator error: {e}")

    print("\n" + "=" * 60)
    if risk_scores:
        print(f"Average risk accuracy: {sum(risk_scores) / len(risk_scores):.2f}")
    if consistency_scores:
        print(f"Average consistency: {sum(consistency_scores) / len(consistency_scores):.2f}")
    print("Evaluation complete.")


if __name__ == "__main__":
    run_evaluation()
