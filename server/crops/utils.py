from server import app
import time
import nexmo


def suggestions():
    client = nexmo.Client(key=app.config['API_KEY'], secret=app.config['API_SECRET_KEY'])
    client.send_message({
        'from': 'Nexmo',
        'to': '918920278726',
        'text': 'Inorganic and organic farming suggestions',
    })
    print("while adding name of crop 150-180 kg N, 70-80 kg P2O5, 70-80 kg K2O and 25 kg ZnSO4 per hectare25-30 cartloads of manure")
    print("Organic: Eu ullamco exercitation pariatur ad dolore minim mollit et dolor et quis ullamco in voluptate.")
    time.sleep(5)
    client.send_message({
        'from': 'Nexmo',
        'to': '918920278726',
        'text': 'Pest attack precautions',
    })
    print("chances of pest attack: est alert Thiodan 35 EC @ 27 ml in 18 litres water\nOrganic:Duis amet voluptate sint proident esse commodo labore ut ea excepteur Lorem officia.")
    time.sleep(5)
    client.send_message({
        'from': 'Nexmo',
        'to': '918920278726',
        'text': 'Harvesting reminder',
    })
    print("time for harvesting: You can check out groups if you want resources. Do not burn the leftovers rather than give it to biogas NGO's. You may get manure and electricity in future! ")

def alerts(_farmer, _days):
    # for each day
    for i in range(_days):
        coordiates = _farmer.location.split(',')
        latitude = float(coordiates[0])
        longitude = float(coordiates[1])
        url = f'http://api.openweathermap.org/data/2.5/forecast?id=524901&daily&lat={latitude}&lon={longitude}&cnt=10&appid=60893ea433ccfef4c74713690c452cc5'
        response = requests.get(url).json()
        if i == 2:
            print('irrigation alert')
        for response_day in response['list']:
            if response_day['wind']['speed'] >= 24.5:
                print('Storm alert')
        time.sleep(5)
    print('test for weather')