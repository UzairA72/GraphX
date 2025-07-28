import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np

client=MongoClient('mongodb+srv://ua7088:n2iqvV6f1NxqwXga@database.68msv4d.mongodb.net/?retryWrites=true&w=majority&appName=database')
db = client["users_database"]
collection=db["user"]
collection.create_index("scores")

userid=""   
userrole="Student"

def main_screen(loggedinuser):

    global userid
    userid=loggedinuser #carries over the signed-up/logged in user to store data to their record



    def plot():

        equation=equation_entry.get()
        scale=scale_entry.get()
        translation=transformation_entry.get()

        x=np.linspace(-50,50,500)

        try:
            y=eval(equation)
        except:
            tk.messagebox.showerror("Error","Invalid equation, refer to the information button")

        scalefactor=1 # default values
        translationfactor=0

        if scale:
            try:
                scalefactor=float(scale)
            except:
                tk.messagebox.showerror("Error","Invalid scale value!")

        if translation:
            try:
                translationfactor=float(translation)
            except:
                tk.messagebox.showerror("Error","Invalid translation value!")

        transformedy = scalefactor*eval(equation.replace("x",f"(x+{translationfactor})")) #performs the manipulation on the equation

        axes.clear()

        axes.set_xlim([-10,10]) # both these limits set the initial view of the graph
        axes.set_ylim([-10,10])
        axes.plot(x , y,label=f"f(x) = {equation}", color="blue")
        axes.plot(x, transformedy,label=f"{scalefactor}*f(x+{translationfactor})",color="red")
        axes.set_title("GraphX")
        axes.set_xlabel("X-Axis")
        axes.set_ylabel("Y-Axis")
        axes.legend()
        axes.grid()
        axes.axhline(0,color="black",linewidth=1)
        axes.axvline(0,color="black",linewidth=1)

        graph.draw()

        recenteq.insert(0,equation)



    main_page=tk.Tk()   #setting up the base window
    main_page.title("Home")
    main_page.geometry("1050x800")
    main_page.iconbitmap("logo.ico")


    navbar= ttk.Notebook(main_page)
    navbar.pack(fill="both")

    home_tab=ttk.Frame(navbar)  #navigation
    exam_tab=ttk.Frame(navbar)
    data_tab=ttk.Frame(navbar)
    settings_tab=ttk.Frame(navbar)

    navbar.add(home_tab, text="Home")
    navbar.add(exam_tab, text="Exam")
    navbar.add(data_tab, text="Data Centre")
    navbar.add(settings_tab, text="Settings")

    navbar.select(home_tab)
    

    ribbon_frame= tk.Frame(home_tab, height=5, bg="lightgray")
    ribbon_frame.pack(side="top",fill="x")

    def settings_setup():
        main_page.destroy()
        settings()

    def datapage_setup():
        main_page.destroy()
        data_centre()

    def exam_setup():      
        main_page.destroy()
        exam_screen()

    def tab_change(event):
        selected_tab = event.widget.tab(event.widget.index("current"), "text") 

        if selected_tab=="Settings":
            settings_setup()

        if selected_tab=="Data Centre":
            datapage_setup()

        if selected_tab=="Exam":
            exam_setup()
        
    navbar.bind("<<NotebookTabChanged>>", tab_change)

    def info():
        tk.messagebox.showinfo("Help","Equations should be entered in a format where powers are written using x**n and coefficients are written as n*x. For example, the equation y=x²+2x should be entered as x**2 + 2*x")

    header_frame=tk.Frame(main_page)
    header_frame.pack(side="top",anchor="nw",fill="x",padx=10,pady=10)
    
    
    info_button=tk.Button(header_frame,text="Help ⓘ",command=info)
    info_button.pack(side="left",padx=(0,10))
    

    input_frame=tk.Frame(main_page)
    input_frame.pack(side="left", anchor="n", padx=20, pady=100)

    tk.Label(input_frame, text="Enter Equation:", font =("Arial Bold", 16)).grid(row=0, column=0, padx=0, pady=0)
    equation_entry = tk.Entry(input_frame)
    equation_entry.grid(row=1,column=0,padx=0,pady=(0))


    tk.Label(input_frame, text="Scale:", font =("Arial Bold", 12)).grid(row=3, column=0, padx=0, pady=5)
    scale_entry = tk.Entry(input_frame,width=10)
    scale_entry.grid(row=4,column=0,padx=0,pady=5)

    tk.Label(input_frame, text="Translation:", font =("Arial Bold", 12)).grid(row=5, column=0, padx=0, pady=0)
    transformation_entry = tk.Entry(input_frame,width=10)
    transformation_entry.grid(row=6,column=0,padx=0,pady=(5,20))

    tk.Button(input_frame, text="Plot", font=("Arial Bold",12), command=plot).grid(row=7,column=0, padx=5, pady=(10))


    tk.Label(input_frame,text="Recent Equations:",font = ("Arial Bold", 16)).grid(row=8, column=0,padx=20,pady=(100,10))
    recenteq=tk.Listbox(input_frame,height=5, width=40)
    recenteq.grid(row=9, padx=20, pady=30)


    fig, axes=plt.subplots(figsize=(6,5))   #implementing graphing
    graph=FigureCanvasTkAgg(fig,master=main_page)
    graph.get_tk_widget().pack(side="right", fill=tk.BOTH, expand=True)

    navigation= NavigationToolbar2Tk(graph, main_page)
    navigation.update()
    graph.get_tk_widget().pack(side="top", fill=tk.BOTH, expand=True)


    

    main_page.mainloop()



def exam_screen():
    exam_window=tk.Tk()
    exam_window.title("Exam Centre")
    exam_window.geometry("800x400")
    exam_window.iconbitmap("logo.ico")
    

    navbar= ttk.Notebook(exam_window)
    navbar.pack(fill="both")

    home_tab=ttk.Frame(navbar)
    exam_tab=ttk.Frame(navbar)
    data_tab=ttk.Frame(navbar)
    settings_tab=ttk.Frame(navbar)

    navbar.add(home_tab, text="Home")
    navbar.add(exam_tab, text="Exam")
    navbar.add(data_tab, text="Data Centre")
    navbar.add(settings_tab, text="Settings")

    navbar.select(exam_tab)

    def settings_setup():
        exam_window.destroy()
        settings()
    
    def datapage_setup():
        exam_window.destroy()
        data_centre()

    def main_setup():
    
        exam_window.destroy()
        main_screen(userid)


    def tab_change(event):
        selected_tab = event.widget.tab(event.widget.index("current"), "text") 

        if selected_tab=="Home":
            main_setup()
        if selected_tab=="Data Centre":
            datapage_setup()
        if selected_tab=="Settings":
            settings_setup()




    navbar.bind("<<NotebookTabChanged>>", tab_change)

     


    def setup_test(difficulty,photos,wordedquestions,answers_a,answers_b,answers_c,answers_d,correct_answers):  #assessment algorithm
        global n
        n=1
        global score
        score=0

        exam_window.destroy()

        test_window=tk.Tk()
        test_window.title(f"{difficulty} [Assessment]")
        test_window.geometry("850x620")
        test_window.iconbitmap("logo.ico")
        


        def end_of_quiz():
            test_window.geometry("800x400")
            notice = tk.Label(test_window,text="You have reached the end of this assessment",font=("Arial Bold",16))
            notice.pack(pady=(50,0))
            score_display=tk.Label(test_window,text=f"Score: {score} out of 4",font=("Arial Bold", 14))
            score_display.pack(pady=(30,0))

            retry_button=tk.Button(test_window,text="Retry",font=("Arial Bold",12), command=retry_quiz)
            retry_button.pack(pady=(80,0))

            exit_button=tk.Button(test_window,text="Save & Exit",font=("Arial Bold",12), command=save_exit)
            exit_button.pack(pady=(50,0))

        def retry_quiz():
            global n
            n=1
            global score
            score=0
            for widget in test_window.winfo_children():
                widget.destroy()
            test_window.geometry("850x600")
            question(n)
        
        def save_exit():
            collection.update_one({"_id":userid},{"$push":{"quiz_scores":f"{difficulty}:{((score/4)*100)}%"}})
            test_window.destroy()
            exam_screen()

        def check_answer(given_answer,index):
            if given_answer == correct_answers[index]:
                global score
                score+=1
                tk.messagebox.showinfo("Info","Answer has been recorded")
                next_question()
            else:
                tk.messagebox.showinfo("Info","Answer has been recorded")
                next_question()

        def skip_question():
            confirmation=tk.messagebox.askyesno("Confirmation","Do you wish to skip this question?")
            if confirmation == True:
                next_question()

        def next_question():
            global n
            n=n+1
            for widget in test_window.winfo_children():
                widget.destroy()
            if n <= 4:
                question(n)
            else:
                end_of_quiz()

        def question(current_question):
            tk.Label(test_window, text=f"{difficulty}", font=("Arial Bold", 16)).pack(pady=(30,0))

            progress=tk.Label(test_window, text=f"Question:{current_question}/4", font=("Arial Bold", 12))
            progress.pack(side="top",padx=10, anchor="nw",pady=(50,0))

            next_button=tk.Button(test_window, text="⏩",width=5,command=skip_question)
            next_button.pack(side="top",padx=10,anchor="ne")

            display_question=tk.PhotoImage(file=f"{photos[current_question-1]}")
            display=tk.Label(test_window,image=display_question)
            display.image = display_question
            display.pack()

            display_worded_question=tk.Label(test_window,text=f"{wordedquestions[current_question-1]}",font=("Verdana",9),wraplength=800)
            display_worded_question.pack(pady=(20,30))

            multiplechoice_frame= tk.Frame(test_window)
            multiplechoice_frame.pack(side="bottom", pady=20)

            index=current_question-1

            answer_a=tk.Button(multiplechoice_frame,text=f"A ┃ {answers_a[current_question-1]}",command = lambda: check_answer(answers_a[index],index))
            answer_a.grid(row=0, column=0, padx=10)

            answer_b=tk.Button(multiplechoice_frame,text=f"B ┃ {answers_b[current_question-1]}",command = lambda: check_answer(answers_b[index],index))
            answer_b.grid(row=0, column=1, padx=10)
            
            answer_c=tk.Button(multiplechoice_frame,text=f"C ┃ {answers_c[current_question-1]}",command=  lambda: check_answer(answers_c[index],index))
            answer_c.grid(row=0,column=2,padx=10)

            answer_d=tk.Button(multiplechoice_frame,text=f"D ┃ {answers_d[current_question-1]}",command=  lambda: check_answer(answers_d[index],index))
            answer_d.grid(row=0, column=3, padx=10)
            
            

            current_question+=1


        question(n)

        exam_window.mainloop()

    def beginner_test():
        setup_test("Beginner",
        ["question1.png","question2.png","question3.png","question4.png"],
        ["Given that the original function y=f(x) [Blue] underwent a stretch parallel to the y-axis of scale factor 6, what is the equation of the translated curve [Red]?",
         "Given that the original function y=f(x) [Blue] underwent a translation by (-6,0), what is the equation of the translated curve [Red]?",
         "Given that the origninal function y=f(x) [Blue] was reflected in the x-axis by scale factor 1, what is the equation of the resultant curve [Red]?",
         "Given that the original function y=f(x) [Blue] was reflected in the x-axis by scale factor 1/2, what is the equation of the resultant curve [Red] ?"],
        ["y=6f(x)","y=f(x-1/6)","y=f(x-1)","y=1/2f(-x)"],
        ["y=1/6f(x)","y=f(x-6)","y=f(-x)","y=-1/2f(x)"],
        ["y=f(x+6)","y=-6f(x)","y=-f(x)","y=f(x-1/2)"],
        ["y=f(x-6)","y=f(x+6)","y=f(x)-2","y=f(x)-1/2"],
        ["y=1/6f(x)","y=f(x+6)","y=-f(x)","y=-1/2f(x)"])
    def intermediate_test():
        setup_test("Intermediate",
        ["question5.png","question6.png","question7.png","question8.png"],
        ["The original function y=f(x) [Blue] underwent a vertical stretch by scale factor 1.5 and a horizontal shift by scale factor 2 to produce a new curve y=g(x) [Red]. Express g(x) in terms of a translation of f(x)",
         "The curve f(x) [Blue] was reflected in the x-axis with scale factor 1 and translated 2 units to the left to produce the new curve y=af(x+b) [Red]. Select the correct equation for the translated curve",
         "The curve f(x)=e**x [Blue] undergoes a vertical reflection by scale factor 0.5 and a shift by 7/2 units in the positive x-direction. What is the equation of the new curve [Red] in terms of f(x)?",
         "The function y=log(x) [Blue] undergoes a shift in the x-direction 3 units to the left and is reflected in the x-axis. Select the equation of the resultant curve [Red]"],
        ["y=-1.5f(x-2)","y=-f(x+2)","1/2f(x-1.4)","y=f(x-3)"],
        ["y=1.5f(x-2)","y=2f(x-1)","1.4f(x-1/2)","y=-f(x+3)"],
        ["y=1.5f(x+2)","y=f(x-2)-1","-0.5f(x+1.4)","y=f(x+3)"],
        ["y=2/3f(x+2)","y=f(x+1)","-1/2f(x+1.2)","y=f(x+3)-1"],
        ["y=1.5f(x+2)","y=-f(x+2)","-0.5f(x+1.4)","y=-f(x+3)"])
        

    tk.Label(exam_window, text="Select an exam", font=("Arial Bold",16)).pack(pady=(50,0))
    

    ribbon_frame= tk.Frame(home_tab, height=5, bg="lightgray")
    ribbon_frame.pack(side="top",fill="x")
    

    beginner_button = tk.Button(exam_window, text="Beginner                 ☆", padx=90, font=("Arial",12), command=beginner_test)
    beginner_button.pack(pady=(50,0))

    intermediate_button=tk.Button(exam_window, text="Intermediate        ☆☆", padx=90, font=("Arial",12), command=intermediate_test)
    intermediate_button.pack(pady=(30,0))

    fluent_button=tk.Button(exam_window, text="Fluent               ☆☆☆", padx=90, font=("Arial",12))
    fluent_button.pack(pady=(30,0))

    navbar= ttk.Notebook(exam_window)
    navbar.pack(fill="both")


    ribbon_frame= tk.Frame(home_tab, height=5, bg="lightgray")
    ribbon_frame.pack(side="top",fill="x")

    exam_window.mainloop()


def data_centre():
    centre_page=tk.Tk()
    centre_page.title("Data Centre")
    centre_page.geometry("850x650")
    centre_page.iconbitmap("logo.ico")

    navbar=ttk.Notebook(centre_page)
    navbar.pack(fill="both")

    home_tab=ttk.Frame(navbar)
    exam_tab=ttk.Frame(navbar)
    data_tab=ttk.Frame(navbar)
    settings_tab=ttk.Frame(navbar)

    navbar.add(home_tab, text="Home")
    navbar.add(exam_tab, text="Exam")
    navbar.add(data_tab, text="Data Centre")
    navbar.add(settings_tab, text="Settings")

    navbar.select(data_tab)
    

    ribbon_frame= tk.Frame(home_tab, height=5, bg="lightgray")
    ribbon_frame.pack(side="top",fill="x")

    def settings_setup():
        centre_page.destroy()
        settings()

    def exam_setup():      
        centre_page.destroy()
        exam_screen()
    def main_setup():
        centre_page.destroy()
        main_screen(userid)
    

    def tab_change(event):
        selected_tab = event.widget.tab(event.widget.index("current"), "text")
        if selected_tab=="Home":
            main_setup()
        if selected_tab=="Exam":
            exam_setup()
        if selected_tab=="Settings":
            settings_setup()
        
    navbar.bind("<<NotebookTabChanged>>", tab_change)

    def validation(userid):
        user=collection.find_one({"_id":userid})
        role=user.get("role")
        if role == "Student":
            tk.messagebox.showerror("Error","You do not have access to this page")
            centre_page.destroy()
            main_screen(userid)
        elif role=="Teacher":
            global userrole
            userrole="Teacher"
        else:
            tk.messagebox.showerror("Error","You do not have access to this page, contact IT for further support")  #this is for users with "pending verification" status on their account
            centre_page.destroy()
            main_screen(userid)
    
    
    validation(userid)



    def view_data():
        if userrole=="Teacher":
            teacher=collection.find_one({"_id":userid})
            teacher_class=teacher.get("class")


            tk.Label(centre_page,text=f"Class Overview - {teacher_class}",font=("Arial Bold",16)).pack(pady=(30,0))

            students = collection.find({"role":"Student","class":teacher_class})

            data_frame = tk.Frame(centre_page)
            data_frame.pack(anchor="center",pady=(30,0))

            data_frame.grid_columnconfigure(0, weight=1, uniform="equal") #allows the data to wrap evenly around the page
            data_frame.grid_columnconfigure(3, weight=1, uniform="equal") 



            header_name = tk.Label(data_frame,text="Name",font=("Arial Bold", 14),anchor="w")
            header_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            header_scores = tk.Label(data_frame,text="Scores",font=("Arial Bold", 14),anchor="e")
            header_scores.grid(row=0, column=3, padx=10, pady=10, sticky="e")


            
            for row, student in enumerate(students,start=1): #iterates through all students in the class to show data
                firstname=student['firstname']
                lastname=student['lastname']
                quiz_scores=student.get('quiz_scores')

                display_student=tk.Label(data_frame, text=f"{firstname} {lastname}", font=("Arial",12),anchor="w")
                display_student.grid(row=row, column=0,padx=10,pady=5,sticky="w")

                display_score=tk.Label(data_frame,text=f"{','.join(quiz_scores)}",font=("Arial",12),anchor="e",wraplength=750)
                display_score.grid(row=row,column=3,padx=10,pady=5,sticky="e")
            
            


    view_data()


    centre_page.mainloop()



def settings():
    settings_page=tk.Tk()
    settings_page.title("Settings")
    settings_page.geometry("500x500")
    settings_page.iconbitmap("logo.ico")

    navbar=ttk.Notebook(settings_page)
    navbar.pack(fill="both")

    home_tab=ttk.Frame(navbar)
    exam_tab=ttk.Frame(navbar)
    data_tab=ttk.Frame(navbar)
    settings_tab=ttk.Frame(navbar)

    navbar.add(home_tab, text="Home")
    navbar.add(exam_tab, text="Exam")
    navbar.add(data_tab, text="Data Centre")
    navbar.add(settings_tab, text="Settings")

    navbar.select(settings_tab)
    

    ribbon_frame= tk.Frame(settings_tab, height=5, bg="lightgray")
    ribbon_frame.pack(side="top",fill="x")
    
    def data_setup():
        settings_page.destroy()
        data_centre()

    def exam_setup():      
        settings_page.destroy()
        exam_screen()
    def main_setup():
        settings_page.destroy()
        main_screen(userid)
    

    def tab_change(event):
        selected_tab = event.widget.tab(event.widget.index("current"), "text")
        if selected_tab=="Home":
            main_setup()
        if selected_tab=="Exam":
            exam_setup()
        if selected_tab=="Data Centre":
            data_setup()
        
    navbar.bind("<<NotebookTabChanged>>", tab_change)

    user=collection.find_one({"_id":userid})
    username=user.get("username")
    classname=user.get("class")
    role=user.get("role")
    tk.Label(settings_page,text="Manage Account",font=("Arial Bold",18)).pack(pady=(30,0))

    def save():
        confirmed=tk.messagebox.askyesno("Confirmation",f"Do you wish to set your class to {class_entry.get().upper()}")
        if confirmed:
            collection.update_one({"_id":userid},{"$set":{"class":class_entry.get().upper()}})
            tk.messagebox.showinfo("Success",f"{username}'s class has been updated")



    data_frame=tk.Frame(settings_page)
    data_frame.pack(pady=(30,0))

    tk.Label(data_frame,text="User:",font=("Arial Bold",16)).grid(row=0,column=0,padx=10,pady=10)
    tk.Label(data_frame,text=f"{username}",font=("Arial",14)).grid(row=0,column=1,padx=10,pady=10)

    tk.Label(data_frame,text="Role:",font=("Arial Bold",16)).grid(row=1,column=0,padx=10,pady=10)
    tk.Label(data_frame,text=f"{role}",font=("Arial",14)).grid(row=1,column=1,padx=10,pady=10)

    tk.Label(data_frame,text="Class:",font=("Arial Bold",16)).grid(row=2,column=0,padx=10,pady=10)
    tk.Label(data_frame,text=f"{classname}",font=("Arial",14)).grid(row=2,column=1,padx=10,pady=10)

    tk.Label(settings_page,text="Link to Class:",font=("Arial Bold",14)).pack(anchor="s",pady=(30,10))
    class_entry=tk.Entry(settings_page,width=10)
    class_entry.pack(anchor="s",pady=(10,10))

    save_button=tk.Button(settings_page,text="Save",font=("Arial Bold",14),command=save,width=10)
    save_button.pack(anchor="s",pady=(20,30))
    settings_page.mainloop()

    






