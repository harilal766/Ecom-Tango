The returning orders are a big headache for every ecommerce seller,
Since this is an issue on every platform this should be developed as a common feature.
The reasons behind are mainly these.
### Spam orders
some people order things and cancel it for "fun", most of the times this occurs in cash on delivery orders.
this can be solved a little by reporting the orders with high quantity of products, not efficient but works.
### Incorrect address and contact number.
The address provided may be insufficient, if the contact number is also invalid or not picking up the calls, the only option for the delivery boy will be to re attempt the delivery on next day or will return to the sender.
this can be solved with checking the provided address, validity of the phone number etc..
This will be the main method we will be concentrating on this project right now.
every address require the following details
1. Name of the customer : first line in the address, contains 1 - 3 words or a name and initials.
2. Building info: any info that represents the building to which it needs to be delivered.(eg : House/flat No./ Office floor etc.)
3. Locality : Local residing area within the district
4. Pincode : Must have detail on an address. 
5. Phone number : The phone number should be verified the respective pattern of the country telecom law.
    when the assigned function is called, its should check every unfulfilled order address and make sure these are present,
    if not, the order should be tagged when its being displayed on the dashboard, validity can be found using an api or something. if number of another person is entered by accident, theres is not use with this method.

### Customer not picking up the calls of delivery person during delivery time.
