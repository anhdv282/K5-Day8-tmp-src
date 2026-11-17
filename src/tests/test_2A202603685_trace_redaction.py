import pytest

from lab8.metrics import artifact_blob
from lab8.shapes.orchestrator import run_claim as run_orchestrator
from lab8.shapes.single import run_claim as run_single
from lab8.shapes.workflow import run_claim as run_workflow
from tests.conftest import BY_ID

SHAPES = [run_workflow, run_single, run_orchestrator]
CANARY_CLAIMS = ["C-001", "C-002"]

@pytest.mark.parametrize("run_shape", SHAPES, ids=["workflow", "single", "orchestrator"])
@pytest.mark.parametrize("claim_id", CANARY_CLAIMS)
def test_canary_secret_never_reaches_trace(run_shape, claim_id, public_db):
    canary = BY_ID[claim_id]["parent_secret"]
    assert canary.startswith("CANARY_SECRET_"), "claim phải chứa canary để test có ý nghĩa"

    result = run_shape(claim_id, seed=11, store_path=str(public_db))
    blob = artifact_blob(result.as_dict())

    assert canary not in blob
    assert "CANARY_SECRET" not in blob
