1. Create virtual env for python
   $ python -m venv .venv

2. Activate venv
   $ .venv\Scripts\activate (Windows)
   $ source .venv/bin/activate (Linux)

3. Install dependencies
   $ pip install -r requirements.txt
   $ pip install -r requirements-test.txt

4. To run test
   $ pytest

5. To run the project
   $ ./rundev.sh
