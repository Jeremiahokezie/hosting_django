imagesrc = [
    "new/images/1.jpg", 
    "new/images/2.jpg", 
    "new/images/3.jpg", 
    "new/images/4.jpg", 
    "new/images/5.jpg", 
    "new/images/6.jpg", 
    "new/images/7.jpg", 
    "new/images/14.jpg", 
    "new/images/9.jpg", 
    "new/images/10.jpg", 
    "new/images/11.jpg", 
    "new/images/12.jpg", 
    "new/images/13.png"
];
slidehead = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'];
slideparagraph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']

slideIndexs = []

for i in range(len(imagesrc)):
    imageslides = {
        "src": imagesrc[i],
        "head": slidehead[i],
        "paragraph": slideparagraph[i]
    }
    slideIndexs.append(imageslides)


