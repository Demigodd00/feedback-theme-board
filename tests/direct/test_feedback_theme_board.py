from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "feedback_theme_board.py"
SDK = "v0.2.16"
PROMPT = "Classify one feedback entry"
STANDARD = "Assign the closest explicit theme using only the submitted feedback and frozen theme descriptions. Do not infer identity, emotion, urgency, or medical risk."


def deploy(vm, direct_deploy, owner):
    vm.sender = owner
    return direct_deploy(str(CONTRACT), "What should the community workshop improve for the next monthly session?", STANDARD, sdk_version=SDK)


def prepare(contract, vm, owner, second, third):
    contract.add_theme("ACCESS", "Access to the room, entry instructions, seating, and physical setup for participants.")
    contract.add_theme("MATERIALS", "Handouts, tools, examples, and other learning materials used during the workshop.")
    contract.open_feedback()
    contract.submit_feedback("f1", "The side-door code expires Friday, so the host must send a new entry code before Saturday's workshop.")
    vm.sender = second
    contract.submit_feedback("f2", "The printed exercise sheet should include one complete worked example before the next session.")
    vm.sender = third
    contract.submit_feedback("f3", "A larger sign near the side entrance would make the regular arrival route easier to spot.")
    vm.sender = owner
    contract.lock_feedback()


def test_classification_vote_and_priority(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    direct_vm.mock_llm(PROMPT, json.dumps({"theme_id": "ACCESS"}))
    contract.classify_feedback("f1")
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"theme_id": "MATERIALS"}))
    assert direct_vm.run_validator(leader_result=leader) is False
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"theme_id": "MATERIALS"}))
    contract.classify_feedback("f2")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"theme_id": "ACCESS"}))
    contract.classify_feedback("f3")
    contract.vote_priority("ACCESS")
    direct_vm.sender = direct_bob
    contract.vote_priority("MATERIALS")
    direct_vm.sender = direct_charlie
    contract.vote_priority("ACCESS")
    direct_vm.sender = direct_alice
    contract.finalize_board()
    assert contract.get_state()["priority_theme"] == "ACCESS"
    assert contract.get_theme("ACCESS")["classified_count"] == 2


def test_one_feedback_per_address_and_facilitator_controls_lock(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.add_theme("ACCESS", "Entry, seating, and room-access feedback for the workshop.")
    contract.add_theme("MATERIALS", "Handouts, tools, and example-material feedback for the workshop.")
    contract.open_feedback()
    direct_vm.sender = direct_bob
    contract.submit_feedback("one", "The entry instructions should name the side door and show the current access code before the session.")
    with direct_vm.expect_revert("one_feedback_entry_per_address"):
        contract.submit_feedback("two", "A second feedback item from the same address must not enter this bounded board.")
    with direct_vm.expect_revert("only_facilitator"):
        contract.lock_feedback()


def test_invalid_theme_from_model_preserves_submission(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    direct_vm.mock_llm(PROMPT, json.dumps({"theme_id": "SECRET"}))
    with direct_vm.expect_revert("invalid_theme"):
        contract.classify_feedback("f1")
    assert contract.get_feedback("f1")["state"] == "SUBMITTED"
    assert contract.get_state()["classified_count"] == 0
