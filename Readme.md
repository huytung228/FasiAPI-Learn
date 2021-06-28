# Setup
python -m venv {name_venv}
source {name_venv}/bin/activate
pip install fastapi
pip install uvicorn

# What learned?
- Path parametters
    - Cast type for params: e.x: (id: int)
    - Note: Order matters
- Query parametters
    - Catch query parametters in child function
    - Cast datatype
    - Optional      
- Request body: Send data from client to API
    - Need 'pydantic' model
- Debugging
- Pydantic Schemas
