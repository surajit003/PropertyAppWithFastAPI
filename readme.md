#Use case

An organization called Test Org comes to a property management company. The property management
investigates the property and determines a rate and sends the organization a quotation.
Upon agreement, the property management Co sends a payment link for the organization to make the
payment. The Organization makes the payment and a payment record is saved in the Database

# Task checklist Link
    -task_checklist.md

# Quick Set up
   - pip install -r requirements.txt
   - create .env file and add the keys for env-example
   - alembic upgrade head (to migrate)
   - uvicorn main:app --reload (to run server)