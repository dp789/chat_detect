import tkinter as tk

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    
    def __init__(self, *args, **kwargs):

        excludearr = []
        Page.__init__(self, *args, **kwargs)
        f = open("flagged_messages.txt")
        s = f.readlines()
        f.close()

        f22 = open("flagged.txt")
        s2 = f22.readlines()
        f22.close()
        temp = ""
        for st in s2:
            if st == "\n" and temp != "\n" and temp != "":
                excludearr.append(temp)
                print(temp)
                temp = ""
            else:
                temp = temp + st
        i = 0
        curr = ""
        def dothework():
            print("hi")
            f = open("flagged.txt", "a")
            ind = 0
            for i in var1:
                print(i.get() == 1)
                if(i.get()):
                    c1[ind].destroy()
                    st = valu[ind]
                    print(st)
                    f.write(st + "\n")
                ind += 1
            f.close()



        val = []
        c1 = []
        var1 = []
        valu = []
        x = {}
        for st in s:
            f = 0
            for j in excludearr:
                print(j.strip())
                print("hi")
                print(curr.strip())
                if curr.strip() == j.strip():
                    f = 1
            if f == 1:
                curr = ""
                continue
            if st == "\n" and curr != "\n" and curr != "":
            # label = tk.Label(self, text=url + "    " + count + " malicious words")
                var1.append(tk.IntVar())
                valu.append(curr)
                c1.append(tk.Checkbutton(self, text = curr, variable = var1[i], onvalue = 1, offvalue = 0))
                i += 1
                c1[i - 1].pack()
                curr = ""
            else:
                curr = curr + st
        b = tk.Button(self, text = "Flag as false positive", command = dothework)
        b.pack()


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        f = open("websites_ranked.txt")
        s = f.readlines()
        f.close()
        i = 0
        for st in s:
            l = st.split(' ')
            url = l[0]
            count = l[1]
            # label = tk.Label(self, text=url + "    " + count + " malicious words")
            b = tk.Label(self, text = url)
            b.grid(row = i, column = 0, ipadx = 50, ipady = 10)
            b = tk.Label(self, text = count + " malicious words")
            
            b.grid(row = i, column = 1, ipadx = 50, ipady = 10)
            i += 1


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()