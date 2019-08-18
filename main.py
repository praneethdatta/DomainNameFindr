from lib.urlgenerate import Generate

if __name__ == '__main__':
    while(1):
        inp_brand = str(raw_input("Enter Brand Name: ")).lower()
        if inp_brand == 'quit':
            break
        prediction = Generate(inp_brand)
        score, url = prediction.get()
        print "domain: ",url
        print "prediction score: ",score