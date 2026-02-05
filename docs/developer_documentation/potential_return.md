The returning orders are a big headache for every ecommerce seller,


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
4. Pincode : Must have detail on an address. https://api.postalpincode.in/pincode/{pincode}
5. Phone number : The phone number should be verified the respective pattern of the country telecom law.
    when the assigned function is called, its should check every unfulfilled order address and make sure these are present,
    if not, the order should be tagged when its being displayed on the dashboard, validity can be found using an api or something. if number of another person is entered by accident, theres is not use with this method.
    https://pypi.org/project/phonenumbers/
### Customer not picking up the calls of delivery person during delivery time.

## How this can be solved
Since this is an issue on every platform this should be developed as a common feature, 
so there should be a dedicated method to extract address on the order class representing each platform.
this method should return the address in a dictionary type, like this
`
order_address : {
    'name' : 'Jake Ryan',
    'pincode' : '40091',
    'phone' : '+91 12345678',
    'address' : '123 nowhere lane'
}
`
these dictionaries can be provided to the common method.
the common function should check each address and should add a key to store the improper keys themselves
`
verified_address : {
    'store' : '<storename>',
    'order_id'
    'improper_infos' : None / ['phone','pincode']
}
`
these `improper_infos` can be later marked seperately while these addresses are displayed on the potential return section in the dashboard which will help for quick diagnose and correction.