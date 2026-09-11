import sys

sector = sys.argv[1]
operation = sys.argv[2]
#print(sector,operation)
# 1.Farm Key
farm_id = int(input(''))
temp = farm_id
A = temp % 10
temp = temp // 10

B = temp % 10
temp = temp // 10

C = temp % 10
temp = temp // 10

D = temp % 10
temp = temp // 10

E = temp % 10
temp = temp // 10

F = temp % 10


#print(F,E,D,C,B,A)

#2.System Statistics
power = 20 + A * 6 + C * 4 + E * 2

water = 25 + B * 5 + D * 3 + F * 2

contamination = A * B + C * D + E * F

integrity = 100 - contamination + A + F

# 3.Operator Class

if A == F:
    operation_class = 'ROOT'
elif A > F and C > D:
    operation_class = 'HARVESTER'
elif A < F and B > E:
    operation_class = 'SCOUT'
else :
    operation_class = 'TECHNICIAN'

#print(power,water, contamination,integrity,operation_class)

# 4.Farm Network

network_code = (A + B + C + D + E + F) % 4
if network_code ==0:
    network = 'SOLAR'
elif network_code ==1:
    network = 'IRON'
elif network_code ==2:
    network = 'BIO'
elif network_code ==3:
    network = 'WILD'
# print(network)
# 5.Operation Modifiers
if operation =='HARVEST':
    power = power + 5
    contamination = contamination - 5
elif operation =='IRRIGATE':
    water = water + 10
    contamination = contamination + 5
elif operation =='REPAIR':
    power = power + 10
    water = water - 5
    contamination = contamination + 10

if contamination < 0:
    contamination = 0

integrity = 100 - contamination + A + F

# 6.Sector Authorisation
access = 'DENIED'

if sector == 'GREENHOUSE':
    if operation == 'HARVEST':
        if power >= 70 and water >= 60 and contamination < 50:
            access = 'AUTHORISED'
    elif operation == 'IRRIGATE':
        if water >= 80 and integrity >= 70 and contamination < 45:
            access = 'AUTHORISED'
    elif operation == 'REPAIR':
        if power >= 85 and integrity >= 65 and contamination < 55:
            access = 'AUTHORISED'
elif sector == 'FIELD':
    if operation == 'HARVEST':
        if (power >= 50 or water >= 55) and contamination < 65:
            access = 'AUTHORISED'
    elif operation == 'IRRIGATE':
        if water >= 65 and contamination < 70:
            access = 'AUTHORISED'
    elif operation == 'REPAIR':
        if (power >= 70 or integrity >= 75) and contamination < 70:
            access = 'AUTHORISED'
elif sector == 'BIOVAULT':
    if operation == 'HARVEST':
        if (operation_class == 'SCOUT' or operation_class == 'TECHNICIAN') and contamination < 45:
            access = 'AUTHORISED'
    elif operation == 'IRRIGATE':
        if operation_class == 'SCOUT' and water >= 65 and contamination < 40:
            access = 'AUTHORISED'
    elif operation == 'REPAIR':
        if operation_class == 'SCOUT' and power >= 65 and integrity >= 70 and contamination < 35:
            access = 'AUTHORISED'

# 7.Network Effects
if network == 'SOLAR':
    if access == 'DENIED' and power >=90:
        access = 'AUTHORISED'
elif network == 'IRON':
    if integrity < 60:
        access = 'DENIED'
elif network == 'BIO':
    if water >= 90 and contamination <= 25:
        access = 'OVERRIDE'
elif network == 'WILD':
    if sector == 'GREENHOUSE':
        access = 'DENIED'

# 8.Farm Lockdown
if contamination >= 90:
    access = 'LOCKDOWN'

# 9.Risk Level
risk_score = power + water + contamination - integrity
if risk_score >= 180:
    risk = 'CRITICAL'
elif risk_score >= 140:
    risk = 'RED'
elif risk_score >= 100:
    risk = 'AMBER'
else:
    risk = 'GREEN'

# 10.Efficiency Rating
efficiency = (power + water) / 2
bio_modifier = contamination % 7
efficiency = efficiency + bio_modifier * 0.5

# 11.System Tags
farm_code = 'CF-' + str(C) + str(B) + str(A)

profile_tag = network + '-' + operation_class

alert_count = (A % 3) + 1
alert_mark = '*' * alert_count

# Terminal Output
print('=== CYBER FARM // CONTROL TERMINAL ===')
print(f'Farm Code: {farm_code}')
print(f'Sector: {sector}')
print(f'Operation: {operation}')
print(f'Class: {operation_class}')
print(f'Network: {network}')
print(f'Profile: {profile_tag}')
print(f'Power: {power}')
print(f'Water: {water}')
print(f'Contamination: {contamination}')
print(f'Integrity: {integrity}')
print(f'Efficiency: {efficiency}')
print(f'Risk: {risk}')
print(f'Access: {access}')
print(f'Alert: {alert_mark}')
print('=====================================')



