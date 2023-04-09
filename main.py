import requests
from bs4 import BeautifulSoup

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/events")
def get_events():
    url = "https://www.primariadeva.ro/index.php/informatii_publice/evenimente"
    source_code = requests.get(url)
        
    soup = BeautifulSoup(source_code.text, "html.parser")
    events = soup.find_all("div", class_="col-xs-12")

    eventsArray = []
    for event in events:
            eventDict = {}
            data = event.find("div", class_="date")
            if data:
                data = data.text
            else:
                data = ""
            description = event.find("h5")
            if description:
                description = description.text
            else:
                description = ""
            image_div = event.find("div", class_="col-xs-12 col-sm-4 col-md-3 stire")
            if image_div:
                image_link = image_div.find("img").get("src")
            else:
                image_link = ""
            
            if len(data) > 0 and len(description) > 0 and len(image_link) > 0:
                eventDict["data"] = data
                eventDict["description"] = description
                eventDict["image_link"] = image_link
                eventsArray.append(eventDict)
                
    return eventsArray

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
