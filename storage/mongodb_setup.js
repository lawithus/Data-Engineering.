javascript
//Use or create the fraud detection database
use fraud_detection;

//Create the fraud_alerts collection (if not exists)
db.createCollection("fraud_alerts");

//Create an index on application_id for faster lookup
db.fraud_alerts.createIndex({ application_id: 1 });

//Optional: Insert a test alert document
db.fraud_alerts.insertOne({
  application_id: 1234,
  user_id: 42,
  credit_score: 400,
  loan_amount: 18000,
  reason: "High loan with low credit score",
  timestamp: new Date()
});


