# Bank news analysis using Natural Language Processing

**Author**: Levan Tsinadze


## Task

Given a bank news statement, extract **bank rate** and **quantitative easing** (QE) numbers.

```
given bank news: 'The Governor invited the Committee to vote on the proposition that: Bank Rate should be maintained at 0.5%; The Bank of England should maintain the stock of asset purchases financed by the issuance of central bank reserves at £200 billion. Seven members of the Committee (the Governor, Charles Bean, Paul Tucker, Spencer Dale, Paul Fisher, David Miles and Martin Weale) voted in favour of the proposition. Two members of the Committee voted against the proposition. Adam Posen preferred to maintain Bank Rate at 0.5% and increase the size of the asset purchase programme by £50 billion to a total of £250 billion. Andrew Sentance preferred to increase Bank Rate by 25 basis points and to maintain the size of the asset purchase programme at £200 billion. Minutes of the meeting'
get Bank Rate: 0.5%
get QE: £200
```
# API Service usage

## Postman to send GET requests on this url URL 

```
http://207.154.208.17:5000?text=The Governor invited the Committee to vote on the proposition that: Bank Rate should be maintained at 0.5%; The Bank of England should maintain the stock of asset purchases financed by the issuance of central bank reserves at £200 billion. Seven members of the Committee (the Governor, Charles Bean, Paul Tucker, Spencer Dale, Paul Fisher, David Miles and Martin Weale) voted in favour of the proposition. Two members of the Committee voted against the proposition. Adam Posen preferred to maintain Bank Rate at 0.5% and increase the size of the asset purchase programme by £50 billion to a total of £250 billion. Andrew Sentance preferred to increase Bank Rate by 25 basis points and to maintain the size of the asset purchase programme at £200 billion. Minutes of the meeting
```

## Using Curl 
```
curl --request POST \
  --url http://207.154.208.17:5000/ \
  --header 'cache-control: no-cache' \
  --header 'content-type: application/json' \
  --header 'postman-token: fd6efeda-cada-1a5c-4428-881b5a556035' \
  --data '["The Governor invited the Committee to vote on the proposition that: Bank Rate should be maintained at 0.5%; The Bank of England should maintain the stock of asset purchases financed by the issuance of central bank reserves at £200 billion. Seven members of the Committee (the Governor, Charles Bean, Paul Tucker, Spencer Dale, Paul Fisher, David Miles and Martin Weale) voted in favour of the proposition. Two members of the Committee voted against the proposition. Adam Posen preferred to maintain Bank Rate at 0.5% and increase the size of the asset purchase programme by £50 billion to a total of £250 billion. Andrew Sentance preferred to increase Bank Rate by 25 basis points and to maintain the size of the asset purchase programme at £200 billion. Minutes of the meeting"]'
```
    
## Response:
```json
[{"news": "The governor invited the committee to vote on the proposition that: bank rate should be maintained at 0.5%; the bank of england should maintain the stock of asset purchases financed by the issuance of central bank reserves at £200 billion. seven members of the committee (the governor, charles bean, paul tucker, spencer dale, paul fisher, david miles and martin weale) voted in favour of the proposition. two members of the committee voted against the proposition. adam posen preferred to maintain bank rate at 0.5% and increase the size of the asset purchase programme by £50 billion to a total of £250 billion. andrew sentance preferred to increase bank rate by 25 basis points and to maintain the size of the asset purchase programme at £200 billion. minutes of the meeting", "Bank_Rate": "0.5%", "QE": "£200"}]
```
