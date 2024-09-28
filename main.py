import pandas as pd
import tkinter as tk
from tkinter import messagebox
from generate_data import generate_data


def create_gui()->None:
    root = tk.Tk()
    root.title("Генератор датасета")
    root.geometry("600x550")
    root.resizable(False, False)

    tk.Label(root, text="Выберите вероятности для банков и платёжных систем:", font=("Arial", 12, "bold")).pack(pady=10)

    sliders_frame = tk.Frame(root)
    sliders_frame.pack(pady=10)

    slider_values_banks = {
        'Сбербанк': tk.IntVar(value=0),
        'ВТБ': tk.IntVar(value=0),
        'Т-Банк': tk.IntVar(value=0),
        'Альфа-Банк': tk.IntVar(value=0)
    }

    slider_values_payments = {
        'Visa': tk.IntVar(value=0),
        'MasterCard': tk.IntVar(value=0),
        'Мир': tk.IntVar(value=0)
    }

    def update_total()->None:
        total_banks = sum(var.get() for var in slider_values_banks.values())
        total_payment_systems = sum(var.get() for var in slider_values_payments.values())

        total_label_banks.config(text=f"Общая сумма для банков: {total_banks}%")
        total_label_payments.config(text=f"Общая сумма для платёжных систем: {total_payment_systems}%")

        if total_banks > 100:
            total_label_banks.config(fg="red")
        else:
            total_label_banks.config(fg="black")

        if total_payment_systems > 100:
            total_label_payments.config(fg="red")
        else:
            total_label_payments.config(fg="black")

    user_data = {}

    def save_data()->None:
        try:
            bank_probabilities = {bank: var.get() for bank, var in slider_values_banks.items()}
            payment_probabilities = {system: var.get() for system, var in slider_values_payments.items()}

            total_banks = sum(bank_probabilities.values())
            total_payments = sum(payment_probabilities.values())

            if total_banks > 100 or total_payments > 100:
                raise ValueError("Общая сумма процентов не может превышать 100%!")
            elif total_banks < 100 or total_payments < 100:
                raise ValueError("Общая сумма процентов должна составлять 100%!")

            num_rows = int(num_rows_var.get())
            if num_rows < 50000:
                raise ValueError("Количество строк должно быть не менее 50000!")

            user_data['bank_probabilities'] = list(bank_probabilities.values())
            user_data['payment_probabilities'] = list(payment_probabilities.values())
            user_data['num_rows'] = num_rows

            messagebox.showinfo("Успех", "Данные успешно сохранены!")
            root.destroy()

            BANK_PROBABILITIES = user_data['bank_probabilities']
            PAYMENT_SYSTEMS_PROBABILITIES = user_data['payment_probabilities']
            NUM_ROWS = user_data['num_rows']
            df = pd.DataFrame(generate_data(BANK_PROBABILITIES, PAYMENT_SYSTEMS_PROBABILITIES, NUM_ROWS))
            df.to_csv("dataset.csv", index=False)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    banks_frame = tk.Frame(sliders_frame)
    banks_frame.pack(side="left", padx=20)

    payments_frame = tk.Frame(sliders_frame)
    payments_frame.pack(side="right", padx=20)

    tk.Label(banks_frame, text="Банки", font=("Arial", 12, "bold")).pack()
    for bank, var in slider_values_banks.items():
        frame = tk.Frame(banks_frame)
        frame.pack(pady=5, fill='x')

        tk.Label(frame, text=bank, width=15, anchor='w').pack(side='left')
        slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', variable=var,
                          command=lambda val, b=bank: update_total())
        slider.pack(side='left', fill='x', expand=True)

    tk.Label(payments_frame, text="Платёжные системы", font=("Arial", 12, "bold")).pack()
    for system, var in slider_values_payments.items():
        frame = tk.Frame(payments_frame)
        frame.pack(pady=5, fill='x')

        tk.Label(frame, text=system, width=15, anchor='w').pack(side='left')
        slider = tk.Scale(frame, from_=0, to=100, orient='horizontal', variable=var,
                          command=lambda val, s=system: update_total())
        slider.pack(side='left', fill='x', expand=True)

    total_label_banks = tk.Label(root, text="Общая сумма для банков: 0%", font=("Arial", 12))
    total_label_banks.pack(pady=5)

    total_label_payments = tk.Label(root, text="Общая сумма для платёжных систем: 0%", font=("Arial", 12))
    total_label_payments.pack(pady=5)

    tk.Label(root, text="Введите количество строк (не менее 50000):", font=("Arial", 12, "bold")).pack(pady=10)
    num_rows_var = tk.StringVar(value="50000")
    num_rows_entry = tk.Entry(root, textvariable=num_rows_var, font=("Arial", 12))
    num_rows_entry.pack(pady=5)

    save_button = tk.Button(root, text="Сохранить данные и продолжить", command=save_data, bg="green", fg="white",
                            font=("Arial", 12))
    save_button.pack(pady=20)
    update_total()

    root.mainloop()


create_gui()
