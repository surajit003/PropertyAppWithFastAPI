# Task 1 (Done)

     Onboard an organization/company into our system
    - Save organization details in database
    - Save organization details to Hubspot
    
    -Rollback
     if organization creation succeeds in our database but fails in Hubspot
     then the record is deleted from our database to maintain consistency.
    
# Task 2 (Done)

    - Onboard a contact into the system
    - Save Contact details in database
    - Associate contact with the organization
    - Save Contact details in Hubspot

# Task 3 (DONE)

    - Create a Charge into our system for an organization
    - Save Charge details in database
    - Save Charge details in Hubspot

# Task 4 (TODO)

    - Render stripe charge form in charge.html
    - Generate a payment link for that organization
    - Charge a client using Stripe Payment API
    - Use status.html to display payment status to client
    - Save Payment details in the DB for that charge
    - Save Payment details in Hubspot

# Task 5 (DONE)
    - Email API endpoint for sending emails
    - Message Model for saving message record
    - Integrate with Sendgrid API for emailing
    - Save message response in DB

# Task 6 (TODO)

    - Booking appointment for property 
    - Record relevant information for appointment
    - Save in Database
    - Save in Hubspot


# Task 7 (IN PROGRESS)

    - Integrate pytest
    - Add tests for the API endpoints
    - Add tests for the stripe api functionality
    - Add tests for hubspot functions

# Task 7 (DONE)

    - Integrate boto3
    - Push request logs to AWS Dynamo DB
    - Add tests