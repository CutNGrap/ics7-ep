
from tkinter import *
import tkinter as tk
import Input as i
from Table import Table
from functions import *
from PfeFrame import *
root = Tk()
experiment = PfeFrame(root)
label1 = Label(text= "Регрессия")
label2 = Label(text = "Линейная")
label3 = Label(text = "Частично нелинейная")
labelNormLin = Label()
labelNatLin  = Label()
labelNormPart = Label()
labelNatPart = Label()

varList = {
    "lambda": StringVar(),
    "mu": StringVar(),
    "k": StringVar(), 
    "N": StringVar(), 
    "start": StringVar(), 
    "end": StringVar(),
    "N_exp": StringVar(), 
    "lambda_min": StringVar(), 
    "lambda_max": StringVar(),
    "mu_min": StringVar(),
    "mu_max": StringVar(),
}


def work_proc(Event):
    modelling(
        clients_number=float(varList["N"].get())+1000,
        clients_proccessed=float(varList["N"].get()),
        lambda_coming=float(varList["lambda"].get()),
        lambda_obr=float(varList["mu"].get())
    )

def work_view(Event):
    view(
        start=float(varList["start"].get()), 
        end=float(varList["end"].get()), 
        N=float(varList["N_exp"].get())
    )


def one_model_list(root):
    items = [
        i.Item(text="Интенсивность поступления заявок:", var=varList["lambda"], value=10),
        i.Item(text="Интенсивность обслуживания заявок:", var=varList["mu"], value=15),
        i.Item(text="Число заявок:", var=varList["N"], value=1000),
    ]
    i_list = i.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn = Button(root, text="Запуск")
    btn.bind("<Button-1>", work_proc)       
    btn.grid(column=1, padx=10, pady=10)  

def work_pfe(Event):
    try:
        lambda_min = float(varList["lambda_min"].get())
        lambda_max = float(varList["lambda_max"].get())
        mu_min = float(varList["mu_min"].get())
        mu_max = float(varList["mu_max"].get())
        count = float(varList["N"].get())
        experiment.run(
            lambda_min=lambda_min,
            lambda_max=lambda_max,
            mu_max=mu_max,
            mu_min=mu_min, 
            count=count, 
            label1 = labelNormLin,
            label2=labelNormPart,
            label3=labelNatLin,
            label4=labelNatPart
        )        
        add_button.config(state='normal')
    except ValueError:
        tk.messagebox.showinfo(title="error", message="Ошибка ввода параметров!")

def work_one(Event): 
    lam = float(varList["lambda"].get())
    mu = float(varList["mu"].get())
    experiment.count_one(lam=lam, mu=mu,)

def pfe_inputs(root):
    t = tk.Label(root, text="Эксперимент")
    t.grid(column=1,  padx=10, pady=10)
    frame_inputs = Frame(root)
    items_1 = [
        i.Item(text="Минимум:", var=varList["lambda_min"], value=5), 
        i.Item(text="Максимум:", var=varList["lambda_max"], value=35), 
    ]
    items_2 = [
        i.Item(text="Минимум:", var=varList["mu_min"], value=95), 
        i.Item(text="Максимум:", var=varList["mu_max"], value=105), 
    ]
    i_list_1 = i.InputList(master=frame_inputs, items=items_1, title="Интенсивность поступления заявок")
    i_list_2 = i.InputList(master=frame_inputs, items=items_2, title="Интенсивность обработки заявок")

    i_list_1.pack(side=LEFT, padx=10, pady=10)
    i_list_2.pack(side=LEFT,  padx=10, pady=10)

    frame_inputs.grid(column=1)

    items_4 = [
        i.Item(text="Число заявок:", var=varList["N"], value=5000), 
    ]

    i_list_4 = i.InputList(master=root, items=items_4)
    i_list_4.grid(column=1,  padx=10, pady=10)

    btn = Button(root, text="Запуск")
    btn.bind("<Button-1>", work_pfe)
      
    btn.grid(column=1, padx=10, pady=10) 

    label1.grid(column=0, row = 2)
    label2.grid(column=0, row = 3)

    labelNormLin.grid(column=0, row = 4)
    labelNormPart.grid(column = 0, row =5)

    label3.grid(column=0, row = 6)
    labelNatLin.grid(column=0, row = 7)
    labelNatPart.grid(column = 0, row =8)

def draw_new_point(root):
    items = [
        i.Item(text="Интенсивность поступления заявок:", var=varList["lambda"], value=20),
        i.Item(text="Интенсивность обслуживания заявок:", var=varList["mu"], value=100),
    ]
    i_list = i.InputList(master=root, items=items, title="Добавление точки факторного пространства")
    i_list.grid(column=1)

    btn = Button(root, text="Добавить", state=DISABLED)
    btn.bind("<Button-1>", work_one)       
    btn.grid(column=1, padx=10, pady=10)
    btn.config(state="disabled")
    return btn


def expirement_list(root): 
    items = [
        i.Item(text="От:", var=varList["start"], value=0.01), 
        i.Item(text="До:", var=varList["end"], value=1.1), 
        i.Item(text="Число заявок:", var=varList["N_exp"], value=1000)
    ]

    i_list = i.InputList(master=root, items=items)
    i_list.grid(column=1)

    btn2 = Button(root, text="Запуск")
    btn2.bind("<Button-1>", work_view)       
    btn2.grid(column=1, padx=10, pady=10) 

if __name__ == '__main__':
    # f_proc = Frame(root)
    # f_view = Frame(root)

    # one_model_list(f_proc)
    # expirement_list(f_view)

    # f_proc.pack()
    # f_view.pack()

    f_pfe = Frame(root, highlightbackground="lightgrey", highlightthickness=1)
    f_one = Frame(root, highlightbackground="lightgrey", highlightthickness=1)
    pfe_inputs(f_pfe)
    add_button = draw_new_point(f_one)
    f_pfe.grid(row=0, column=0,  padx=10, pady=10)
    f_one.grid(row=0, column=1,  padx=10, pady=10)

    experiment.grid(row=1, column=0, columnspan=2,   padx=10, pady=10)

    root.mainloop()


    def run(self):
        plan_matrix_normalized = self.create_plan_matrix()
        print(plan_matrix_normalized)
        experiment_results = np.zeros(M_SIZE)

        for experiment_number, experiment_params in enumerate(plan_matrix_normalized):
            gen_int = self.natural_factor_from_normalized(experiment_params[1], self.gen_int_min, self.gen_int_max)
            gen_var = self.natural_factor_from_normalized(experiment_params[2], self.gen_var_min, self.gen_var_max)
            proc_int = self.natural_factor_from_normalized(experiment_params[3], self.proc_int_min, self.proc_int_max)

            middle = 1 / gen_int
            range_var = gen_var
            lambda_ = proc_int

            cur_experiment_results = []
            for _ in range(N_REPEATS):
                generators = [Generator(distributions.UniformDistribution(middle, range_var))]
                processors = [Processor(distributions.ExponentialDistribution(lambda_))]
                modeller = Modeller(generators, processors)
                cur_experiment_results.append(modeller.event_modelling(self.requests_amount)['mean_time_in_queue'])

            experiment_results[experiment_number] = sum(cur_experiment_results) / N_REPEATS

        full_results_table, self.coefficients, self.coef_natural = self.process_results(plan_matrix_normalized, experiment_results)

        return full_results_table, self.coefficients, self.coef_natural
