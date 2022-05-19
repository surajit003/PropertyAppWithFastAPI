#Use case

An organization called Test Org comes to a property management company. The property management
investigates the property and determines a rate and sends the organization a quotation.
Upon agreement, the property management Co sends a payment link for the organization to make the
payment. The Organization makes the payment and a payment record is saved in the Database

#Data Store

    - Organization/Company record is saved in a postgres db and Hubspot for business to use.

#Key points to consider

    - Since data is supposed to reside in two places namely postgresql database and Hubspot CRM.
      Data consistency is key and hence the synchronisation of data is a big part of the design.
      Currently, to keep things simple, the process of creating the record is done sequentially.
      However, the plan is to use a event based architecture to decouple the logic.

# Task checklist Link
    -task_checklist.md

# Quick Set up
   - pip install -r requirements.txt
   - create .env file and add the keys for env-example
   - alembic upgrade head (to migrate)
   - uvicorn main:app --reload (to run server)