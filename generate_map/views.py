from django.shortcuts import render, redirect
from django.http import HttpResponse
# importing the module import requests
from typing import Text
import requests;
from PIL import Image
background = Image.new('RGBA', (176, 225), (255,255,255,255))
from PIL import ImageDraw,ImageFont,ImageOps
from io import BytesIO
import numpy as np
import textwrap
import os
from django.conf import settings
from . models import *


BASE_URL = "https://maps.googleapis.com/maps/api/staticmap?"
API_KEY = "AIzaSyCG5HkD6rN79XsC40KMdlELaZvJUMR4_V4"
# lat="30.375321"
# lng="69.34511599999999"
# zoom = 16
# size='1024x1024'
# scale="2"
# shape = "circle" # square || circle
icon_base_url="https://plancoeur.love/wp-content/uploads/icons/"
# marker_enabled=1
marker_url=""


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    # result.paste(pil_img, (left, top))
    return result


def create_map(request, lat, lng, zoom, size, scale, shape, marker_enabled=None):
    marker_name="heart"
    # updating the URL
    style='&style=feature:all|element:geometry.stroke|visibility:simplified&style=feature:administrative|element:all|visibility:off&style=feature:administrative|element:labels|visibility:simplified|color:0xa31645&style=feature:landscape|element:all|weight:3.79|visibility:on|color:0xffecf0&style=feature:landscape|element:geometry|visibility:on&style=feature:landscape|element:geometry.stroke|visibility:on&style=feature:poi|element:all|visibility:simplified|color:0xa31645&style=feature:poi|element:geometry|saturation:0|lightness:0|visibility:off&style=feature:poi|element:geometry.stroke|visibility:off&style=feature:poi.business|element:all|visibility:simplified|color:0xd89ca8&style=feature:poi.business|element:geometry|visibility:on&style=feature:poi.business|element:geometry.fill|visibility:on|saturation:0&style=feature:poi.business|element:labels|color:0xa31645&style=feature:poi.business|element:labels.icon|visibility:simplified|lightness:84&style=feature:road|element:all|saturation:-100|lightness:45&style=feature:road.highway|element:all|visibility:simplified&style=feature:road.arterial|element:labels.icon|visibility:off&style=feature:transit|element:all|visibility:off&style=feature:water|element:all|color:0xd89ca8|visibility:on&style=feature:water|element:geometry.fill|visibility:on|color:0xfedce3&style=feature:water|element:labels|visibility:off'
    URL = BASE_URL + "center=" + lat+","+lng+ "&zoom=" + str(zoom) + "&size="+size+"&key=" + API_KEY +style+"&scale="+scale

    # set market in map
    if(marker_enabled):
        match marker_name:
            case marker_name:
                marker_url=icon_base_url+marker_name+".png"
                URL+="&markers=scale:2anchor:17,34|icon:"+marker_url+"|"+lat+","+lng
    # HTTP request
    response = requests.get(URL)

    im = Image.open(BytesIO(response.content))
    # im = Image.open(URL)

    width, height = im.size   # Get dimensions
    new_width=336+336
    new_height=330 + 330 
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    # im.save('cropped.png')


    # img=Image.open("cropped.png").convert("RGB")
    img = im

    #for
    im_new = add_margin(img, 55, 13, 250, 13, (255, 255, 255))
    # im_new.show()
    # im_new.save('space_added.png', quality=95)


    # im1 = Image.open('space_added.png').convert("RGB")
    # im2 = Image.open('cropped.png').convert("RGB")
    im1 = im_new.convert("RGB")
    im2 = img.convert("RGB")
    W, H = im1.size
    w, h = im2.size
    # print(im1.size)
    # print(im2.size)
    shape1 = [(0,0), (w-0 , w-12)]
    mask_im = Image.new("L", (im2.size), 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse(shape1, fill=255)
    back_im = im1.copy()

    if shape == "circle":
        back_im.paste(im2, ((int((W-w)/2)),25), mask_im)
    else:
        back_im.paste(im2, ((int((W-w)/2)),45))

    back_im.save('circular_added.png', quality=95)
    #It is placing the cropped image on a blank template afrer making it circular

 ## Define fonts
    fonts_array = [["Waltograph UI.ttf", 30], ["Alice-Regular.ttf", 30], ["afterglow-regular.ttf", 30]]
    font_style=1
    match font_style:
        case 1:
                fonts_array = [["alice_movétan.ttf", 29*2], ["poppins-medium.ttf", 21*2], ["alice_movétan.ttf", 21*2]]
        case 2:
                fonts_array = [["alice1.ttf", 29], ["poppins-medium.ttf", 21], ["gentiumplus-regular.ttf", 21]]
        case 3:
                fonts_array = [["afterglow-regular.ttf", 29], ["poppins-medium.ttf", 21], ["gentiumplus-regular.ttf", 20]]
        case 4:
                fonts_array = [["I-found-my-valentine.ttf", 29], ["poppins-medium.ttf", 21], ["gentiumplus-regular.ttf", 20]]
        case 5:
                fonts_array = [["waltographui.ttf", 29], ["poppins-medium.ttf", 21], ["gentiumplus-regular.ttf", 20]]
        case 6:
                fonts_array = [["filxgirl.ttf", 29], ["poppins-medium.ttf", 21], ["gentiumplus-regular.ttf", 20]]
        case 7:
                fonts_array = [["comfortaa-light.ttf", 24], ["poppins-medium.ttf", 21], ["gentiumplus-regular.ttf", 20]]
        

   

    # im = Image.open('circular_added.png')
    im = back_im.convert("RGB")
    title_font = ImageFont.truetype(os.path.dirname(__file__) + '/' + fonts_array[0][0], fonts_array[0][1])
    title_text = "Our first meeting"
    w,h = title_font.getsize(title_text)
    # print(W,H)
    # print(w,h)
    draw = ImageDraw.Draw(im)
    draw.text((int((W-w)/2), H-200), title_text, fill="black", font=title_font)

    title_font = ImageFont.truetype(fonts_array[1][0], fonts_array[1][1])
    title_text = "Emma & Paul"
    w,h = title_font.getsize(title_text)
    draw = ImageDraw.Draw(im)
    draw.text(((int(W-w)/2), H-150), title_text, fill="black", font=title_font)

    title_font = ImageFont.truetype(fonts_array[2][0], fonts_array[2][1])
    title_text = "PARIS"
    w,h = title_font.getsize(title_text)
    # im = Image.open('bkadded.png')
    # im = Image.new("RGBA",(W,600),"yellow")
    draw = ImageDraw.Draw(im)
    # w, h = draw.textlength(title_text)
    draw.text(((int(W-w)/2), H-100), title_text, fill="black", font=title_font)

    # im.show()
    im.save('media/final.png', quality=95)
    try:
        with open('media/final.png', "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response

    #return redirect(f"{settings.DOMAIN_NAME}/media/final.png")