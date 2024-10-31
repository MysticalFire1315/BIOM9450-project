from typing import Dict, Tuple

def create_patient(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    try:
        patient = Patient.new_patient(
            data.get()
        )

        return {
            "status": "success",
            "message": "Successfully created"
        }, 201
    except Exception:
        return {"status": "fail", "message": "Not implemented"}, 400