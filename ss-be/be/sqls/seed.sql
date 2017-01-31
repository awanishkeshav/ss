use ssdb;

insert into ss_txn_category (mccCode,name) values (1000,'Dining');
insert into ss_txn_category (mccCode,name) values (1001,'Entertainment');
insert into ss_txn_category (mccCode,name) values (1002,'Retail');
insert into ss_txn_category (mccCode,name) values (1003,'Travel');
insert into ss_txn_category (mccCode,name) values (1004,'Groceries');
insert into ss_txn_category (mccCode,name) values (1005,'Auto & Gas');
insert into ss_txn_category (mccCode,name) values (1006,'Utilities');
insert into ss_txn_category (mccCode,name) values (1007,'Medical');

#Sample data
## Location
insert into ss_location (name, international) values ('New York', 1);
insert into ss_location (name, international) values ('New Jersey', 1);
insert into ss_location (name, international) values ('New Delhi', 0);
insert into ss_location (name, international) values ('Mumbai', 0);
insert into ss_location (name, international) values ('London', 1);
insert into ss_location (name, international) values ('Pune', 0);
insert into ss_location (name, international) values ('Chennai', 0);
insert into ss_location (name, international) values ('Kolkata', 0);
insert into ss_location (name, international) values ('Paris', 1);
insert into ss_location (name, international) values ('Los Angeles', 1);

## CLIENT
insert into ss_client (name, email, phone, status,token, created, updated)
values ('SBI','sbi@second-swipe.com','9826249953',1,'sbi-token',1423825011000,1423825011000);

## MERCHANT
insert into ss_merchant (name, uuid, email, phone,address, status,lat, lng, reviewStatus,accessCode,installed, mccCode, created, updated)
values ('Fredericos','fredericos','fortune@second-swipe.com','9826249953','341 Grove St, Jersey City, NJ 07032',1,40.72, -74.04, 'RR',
'access-code',1,1000,1423825011000,1423825011000);
insert into ss_merchant (name, uuid, email, phone,address, status,lat, lng, reviewStatus,accessCode,installed, mccCode, created, updated)
values ('Expedia.co.in','expedia-co-in','sbi@second-swipe.com','9826249953','Palasia square, New Delhi',1,28.6, 77.2,'NR','access-code',1,1003,  1423825011000,1423825011000);
insert into ss_merchant (name, uuid, email, phone,address, status,lat, lng, reviewStatus,accessCode,installed, mccCode, created, updated)
values ('Big Bazaar','big-bazaar','satyam@second-swipe.com','9826249953','A.B. Road, Indore',1,22.75, 75.9, 'NR','access-code',1,1004,142382501100,142382501100);
insert into ss_merchant (name, uuid, email, phone,address, status,lat, lng, reviewStatus,accessCode,installed, mccCode, created, updated)
values ('Puma Store','puma-store','sbi@second-swipe.com','9826249953',
'1 Premium Outlet Blvd #571 Tinton Falls, NJ 07032',1,40.72, -74.04, 'RR','access-code',1,1002, 1423825011000,1423825011000);
insert into ss_merchant (name, uuid, email, phone,address, status,lat, lng, reviewStatus,accessCode,installed, mccCode, created, updated)
values ('Indian Oil','indian-oil','sbi@second-swipe.com','9826249953',
'J B Tito Marg, Sadiq Nagar, New Delhi 110049',1,28.61, 77.20, 'RR','access-code',1,1005, 1423825011000,1423825011000);
insert into ss_merchant (name, uuid, email, phone,address, status,lat, lng, reviewStatus,accessCode,installed, mccCode, created, updated)
values ('Shoppers Stop','shoppers-stop','sbi@second-swipe.com','9826249953',
'B/9, Eureka Towers, Mindspace, Malad(w), Mumbai 400064',1,19.1861, 72.848, 'RR','access-code',1,1005, 1423825011000,1423825011000);

## MERCHANT Review
insert into ss_review_template (merchant_id,criteria1, criteria2, criteria3, version,commentRequired,created, updated)
values (1,'Food', 'Service', 'Ambience',1,1,1423825011000,1423825011000);
insert into ss_review_template (merchant_id,criteria1, criteria2, criteria3, version,commentRequired,created, updated)
values (2,'Price', 'Service', 'Quality',1,1,1423825011000,1423825011000);
insert into ss_review_template (merchant_id,criteria1, criteria2, criteria3, version,commentRequired,created, updated)
values (3,'Price', 'Billing time', 'Quality',1,1,1423825011000,1423825011000);
insert into ss_review_template (merchant_id,criteria1, criteria2, criteria3, version,commentRequired,created, updated)
values (4,'Service', 'Billing time', 'Quality',1,1,1423825011000,1423825011000);

## MERCHANT Offer # end date, merchant, category
insert into ss_merchant_offer (title,description,merchant_id,category_id, codeType, code, startDate, endDate, created, updated, distance, status)
values ('Get 20% off your next dinner with us','Offer for 2 people',
1,1,'text','XYABT90',1434204260000, 1435204260000,1423825011000,1423825011000, 0.0,'Active');
insert into ss_merchant_offer (title,description,merchant_id,category_id, codeType, code,  startDate, endDate, created, updated, distance, status)
values ('Get 10% off on flights to Jaipur','Offer for 1 person',2,2,'text','XYABT90',1434204260000, 1432525860000,1423825011000,1423825011000, 0.0,'Active');
insert into ss_merchant_offer (title,description,merchant_id,category_id, codeType, code,   startDate,endDate, created, updated, distance, status)
values ('Get 5% off on this weekend','On all products',
3,3,'text','XYABT90',1434204260000, 1435525860000,1423825011000,1423825011000, 0.0,'Active');
insert into ss_merchant_offer (title,description,merchant_id,category_id, codeType, code,   startDate, endDate, created, updated, distance, status)
values ('Buy one, get one free','For all T-shirts - till May end',
4,4,'text','XYABT90',1434204260000, 1435204260000,1423825011000,1423825011000, 0.0,'Active');
insert into ss_merchant_offer (title,description,merchant_id,category_id, codeType, code,   startDate, endDate, created, updated, distance, status)
values ('10% Off Domestic Airfares','Get 10% off all domestic airfares this summer. Includes flights to Maldives and Nepal.',
2,4,'qr_code','SUMMER10GTR',1429834567745, 1433117525576, 1423825011000,1423825011000, 0.0,'Active');
insert into ss_merchant_offer (title,description,merchant_id,category_id, codeType, code,   startDate, endDate, created, updated, distance, status)
values ('Early Spring Hard Brunch, $29.99','Enjoy your favorite cocktails with a 3 course brunch every weekend in May for just $29.99',
4,4,'bar_code','RTS29',1429842712844, 1433125682233, 1423825011000,1423825011000, 0.0,'Active');

## MErchant offer targetting
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
 1435204260000, 'post_swipe', 1,100,1);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
1435204260000, 'post_review', 1,200,1);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
 1435204260000, 'post_swipe', 1,300,2);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
1435204260000, 'post_review', 1,300,2);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
1435204260000, 'post_swipe', 1,100,3);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
 1435204260000, 'post_review', 1,200,3);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
1435204260000, 'post_swipe', 1,150,4);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
 1435204260000, 'post_review', 1,250,4);
insert into ss_merchant_offer_targetting (created, updated, targetType, minVisits, minTotalSpend, offer_id) values(1435204260000,
 1435204260000, 'existing_customers', 1,250,4);

## CONSUMER ACCOUNT
insert into ss_consumer_account (clientId, cardNum, phoneNum, `limit`,avaialbleLimit, currOS,activationCode,cardNetwork, cardType, cardTitle, created, updated)
values (1, '5242-1651-0012-0554', '9826249935', 200000, 180000, 20000,'pqrs','Master', 'Credit card', 'Classic Card',  1423825011000,1423825011000);
insert into ss_consumer_account (clientId, cardNum, phoneNum, `limit`,avaialbleLimit, currOS,activationCode,cardNetwork, cardType, cardTitle, created, updated)
values (1, '5242-1651-0012-0354', '9826249925', 220000, 190000, 30000,'xyz2','Visa', 'Debit card', 'Silver Card',  1423825011000,1423825011000);
insert into ss_consumer_account (clientId, cardNum, phoneNum, `limit`,avaialbleLimit, currOS,activationCode,cardNetwork, cardType, cardTitle, created, updated)
values (1, '5242-1651-0012-0252', '9826249935', 250000, 235000, 15000,'rajiv','Master', 'Credit card', 'Gold Card',  1423825011000,1423825011000);

## CONSUMER
insert into ss_consumer (firstname, lastname, email, dob,status, lat, lng,blockedCards, blockedMerchants, created, updated)
values ('Dheeraj','Singh','',0,1,10.2, 10.3,'','', 1423825011000, 1423825011000);
insert into ss_consumer (firstname, lastname, email, dob,status, lat, lng, blockedCards, blockedMerchants, created, updated)
values ('Rohit','Sharma','',0,1,10.2, 10.3, '','',1423825011000,1423825011000);
insert into ss_consumer (firstname, lastname, email, dob,status, lat, lng, blockedCards, blockedMerchants, created, updated)
values ('Vijay','Kalra','',0,1,10.2, 10.3, '','',1423825011000,1423825011000);

## CONSUMER DEVICE
insert into ss_consumer_device (consumerId, cardNum, deviceType, deviceSubType,deviceToken,deviceRegistrationId, status, created, updated)
values (1,'5242-1651-0012-0554',1,1,'pqrs',null,1,423825011000,1423825011000);
insert into ss_consumer_device (consumerId, cardNum, deviceType, deviceSubType,deviceToken,deviceRegistrationId, status, created, updated)
values (2,'5242-1651-0012-0354',1,1,'xyz2',null,1, 1423825011000,1423825011000);
insert into ss_consumer_device (consumerId, cardNum, deviceType, deviceSubType,deviceToken,deviceRegistrationId, status, created, updated)
values (3,'5242-1651-0012-0252',1,1,'rajiv',null, 1, 1423825011000,1423825011000);

## CONSUMER CARD
insert into ss_consumer_card (clientId, consumerId,accountId, cardNum, `limit`,avaialbleLimit, currOS,amtSpentSS,cardNetwork, cardType, cardTitle, status, created, updated)
values (1, 1,1, '5242-1651-0012-0554', 200000, 180000, 20000,20000,'Master', 'Credit card', "Classic Card",  1, 1423825011000, 1423825011000);
#insert into ss_consumer_card (clientId, consumerId,accountId, cardNum, `limit`,avaialbleLimit, currOS,amtSpentSS,cardNetwork, cardType, cardTitle, status, created, updated)
#values (1, 2,2, '5242-1651-0012-0354', 220000, 190000 , 30000, 30000,'Visa', 'Debit card', "Silver Card",  1, 1423825011000, 1423825011000);
insert into ss_consumer_card (clientId, consumerId,accountId, cardNum, `limit`,avaialbleLimit, currOS,amtSpentSS,cardNetwork, cardType, cardTitle, status, created, updated)
values (1, 3,3, '5242-1651-0012-0252', 250000, 235000 , 15000, 15000,'Master', 'Credit card', "Gold Card",  1, 1423825011000, 1423825011000);

## Consumer Tag
#insert into ss_consumer_tag (consumerId,tag,created, updated)
#values (1,'Delhi Visit',1423825011000, 1423825011000);
#insert into ss_consumer_tag (consumerId,tag,created, updated)
#values (1,'Chiya''s Birthday',1423825011000, 1423825011000);

## Txn Tag
#insert into ss_txn_tag (cardId,consumerTxn_id,consumerTag_id,created, updated)
#values (1,1,1, 1423825011000,1423825011000);
#insert into ss_txn_tag (cardId,consumerTxn_id,consumerTag_id,created, updated)
#values (1,2,1, 1423825011000,1423825011000);

## Scenario
## ************** Please make sure that mcccode is there in the txn_category table************
INSERT INTO ss_scenario (name, merchantName, merchantUuid, txnType, mccCode, category, location, file) VALUES
('Dine', 'Fredericos', 'fredericos', 'International', '1000', 'Dining', 'New York', 'media/files/dine.png'),
('Travel', 'Flight to Turkey', 'expedia-co-in', 'Online', '1003', 'Travel', 'Expedia.co.in', 'media/files/travel.png'),
('Live', 'Big Bazaar', 'big-bazaar' , 'Card Present', '1004', 'Groceries', 'Gurgaon', 'media/files/live.png'),
('Shop', 'Puma Store', 'puma-store', 'International', '1002', 'Retail', 'New Jersey', 'media/files/shop.png');