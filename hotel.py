import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import datetime
import os
class HotelManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ssp Hotel")
        self.geometry("980x600")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)


        self.guests = []
        self.pickups = []  
        self._next_id = 1
        types = ["Single", "Double", "Deluxe", "Suite"]
        self.rooms = {}
        rn = 101
        for i in range(20):
            self.rooms[rn] = {"type": types[i % 4], "status": "Available", "guest_id": None}
            rn += 1
        self._build_header()
        self._build_left_menu()
        self._build_main_area()
        self.show_new_customer_form()

    def _build_header(self):
        header = tk.Frame(self, bg="#111111", height=70)
        header.pack(fill="x", side="top")
        title = tk.Label(header, text="SSP HOTEL RECEPTION", bg="#111111", fg="#dfe6e9",
                         font=("Times New Roman", 28, "bold"))
        title.pack(pady=12)

    def _build_left_menu(self):
        menu = tk.Frame(self, bg="#111111", width=200)
        menu.pack(side="left", fill="y")

        def mkbtn(text, color, cmd):
            b = tk.Button(menu, text=text, bg=color, fg="#000000", relief="flat",
                          font=("Helvetica", 10, "bold"), command=cmd, height=2)
            b.pack(fill="x", pady=6, padx=8)
            return b

        mkbtn("New Customer Form", "#f4cccc", self.show_new_customer_form)
        mkbtn("Search Room", "#f9cb9c", self.show_search_room)
        mkbtn("Employee Info", "#fff2cc", self.show_employee_info)
        mkbtn("Customer Info", "#d9ead3", self.show_customer_info)
        mkbtn("Check Out", "#c9daf8", self.show_check_out)
        mkbtn("Pickup Service", "#d9d2e9", self.show_pickup_service)
        mkbtn("Update Room Status", "#cfe2f3", self.show_update_room_status)
        mkbtn("Pickup Info", "#f4cccc", self.show_pickup_info)
    def _build_main_area(self):
        self.main_area = tk.Frame(self, bg="#222222")
        self.main_area.pack(side="right", fill="both", expand=True)
        top_frame = tk.Frame(self.main_area, bg="#222222")
        top_frame.pack(fill="x", pady=6)
        self.page_container = tk.Frame(self.main_area, bg="#2b2b2b")
        self.page_container.pack(fill="both", expand=True, padx=12, pady=(6, 12))

    def _clear_page(self):
        for child in self.page_container.winfo_children():
            child.destroy()
    def show_new_customer_form(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True)

        left = tk.Frame(frm, bg="#2b2b2b")
        left.pack(side="left", fill="y", padx=12, pady=12)

        tk.Label(left, text="New Customer Check-In", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(0, 10))

        self.n_name = tk.StringVar()
        self.n_phone = tk.StringVar()
        self.n_roomtype = tk.StringVar(value="Single")

        tk.Label(left, text="Name:", bg="#2b2b2b", fg="#ddd").pack(anchor="w")
        ttk.Entry(left, textvariable=self.n_name, width=30).pack(pady=4)

        tk.Label(left, text="Phone:", bg="#2b2b2b", fg="#ddd").pack(anchor="w")
        ttk.Entry(left, textvariable=self.n_phone, width=30).pack(pady=4)

        tk.Label(left, text="Room Type:", bg="#2b2b2b", fg="#ddd").pack(anchor="w")
        ttk.Combobox(left, values=["Single", "Double", "Deluxe", "Suite"], textvariable=self.n_roomtype,
                     state="readonly", width=28).pack(pady=4)

        ttk.Button(left, text="Assign Room & Check In", command=self._perform_checkin).pack(pady=8)
        ttk.Button(left, text="Reset", command=lambda: [self.n_name.set(""), self.n_phone.set(""), self.n_roomtype.set("Single")]).pack()

        right = tk.Frame(frm, bg="#2b2b2b")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=12)

        tk.Label(right, text="Room Availability Snapshot", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 12, "bold")).pack(anchor="w")

        self.avail_text = scrolledtext.ScrolledText(right, height=14, wrap="word")
        self.avail_text.pack(fill="both", expand=True, pady=(8, 0))
        self._refresh_availability()

    def _perform_checkin(self):
        name = self.n_name.get().strip()
        phone = self.n_phone.get().strip()
        rtype = self.n_roomtype.get().strip()
        if not name or not phone:
            messagebox.showwarning("Missing data", "Please provide both name and phone number.")
            return
        if not phone.isdigit() or len(phone) < 6:
            messagebox.showwarning("Invalid phone", "Please enter a valid phone number (digits only).")
            return

        available_room = None
        for rn, info in sorted(self.rooms.items()):
            if info["type"] == rtype and info["status"] == "Available":
                available_room = rn
                break
        if not available_room:
            messagebox.showinfo("No rooms", f"No available {rtype} rooms at the moment.")
            return

        guest = {"id": self._next_id, "name": name, "phone": phone, "room": available_room,
                 "room_type": rtype, "checkin": datetime.datetime.now()}
        self.guests.append(guest)
        self.rooms[available_room]["status"] = "Occupied"
        self.rooms[available_room]["guest_id"] = guest["id"]
        self._next_id += 1

        messagebox.showinfo("Checked In", f"{name} assigned to room {available_room} ({rtype}).")
        self.n_name.set("")
        self.n_phone.set("")
        self.n_roomtype.set("Single")
        self._refresh_availability()

    def _refresh_availability(self):
        lines = []
        counts = {t: 0 for t in ["Single", "Double", "Deluxe", "Suite"]}
        avail_counts = {t: 0 for t in counts}
        for rn, info in sorted(self.rooms.items()):
            counts[info["type"]] += 1
            if info["status"] == "Available":
                avail_counts[info["type"]] += 1
            lines.append(f"Room {rn}  | {info['type']:6} | {info['status']}")
        summary = " | ".join([f"{t}: {avail_counts[t]}/{counts[t]} available" for t in counts])
        text = summary + "\n\n" + "\n".join(lines)

        self.avail_text.configure(state="normal")
        self.avail_text.delete("1.0", tk.END)
        self.avail_text.insert(tk.END, text)
        self.avail_text.configure(state="disabled")

    def show_search_room(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Search Rooms by Type", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        s_type = tk.StringVar(value="Single")
        ttk.Combobox(frm, values=["Single", "Double", "Deluxe", "Suite"], textvariable=s_type, state="readonly").pack(pady=8)
        res_box = scrolledtext.ScrolledText(frm, height=14)
        res_box.pack(fill="both", expand=True)

        def do_search():
            t = s_type.get()
            lines = []
            for rn, info in sorted(self.rooms.items()):
                if info["type"] == t:
                    lines.append(f"Room {rn} - {info['status']}")
            res_box.delete("1.0", tk.END)
            res_box.insert(tk.END, "\n".join(lines) if lines else "No rooms found.")

        ttk.Button(frm, text="Search", command=do_search).pack(pady=8)

    def show_employee_info(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Employee Information", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        employees = [
            {"name": "Rajesh Kumar", "role": "Manager", "phone": "9876543210"},
            {"name": "Sita Sharma", "role": "Receptionist", "phone": "9123456780"},
            {"name": "Amit Verma", "role": "Housekeeping", "phone": "9988776655"}
        ]

        tree = ttk.Treeview(frm, columns=("role", "phone"), show="headings")
        tree.heading("role", text="Role")
        tree.heading("phone", text="Phone")
        tree.pack(fill="both", expand=True, pady=8)

        for e in employees:
            tree.insert("", tk.END, values=(f"{e['name']} ({e['role']})", e["phone"]))

    def show_customer_info(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Current Customers", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        search_var = tk.StringVar()
        ttk.Entry(frm, textvariable=search_var).pack(anchor="ne", padx=6, pady=6)

        tree = ttk.Treeview(frm, columns=("room", "phone", "checkin"), show="headings")
        tree.heading("room", text="Room")
        tree.heading("phone", text="Phone")
        tree.heading("checkin", text="Checked In")
        tree.pack(fill="both", expand=True, pady=8)

        def refresh_tree(filter_text=""):
            for r in tree.get_children():
                tree.delete(r)
            for g in self.guests:
                if not filter_text or filter_text.lower() in g["name"].lower() or filter_text in str(g["room"]):
                    tree.insert("", tk.END, iid=str(g["id"]), values=(f"{g['room']} ({g['room_type']})", g["phone"], g["checkin"].strftime('%Y-%m-%d %H:%M')))

        search_var.trace_add("write", lambda *args: refresh_tree(search_var.get().strip()))
        refresh_tree()

        def do_checkout():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Select customer", "Please select a customer to check out.")
                return
            cid = int(sel[0])
            self._checkout_by_id(cid)
            refresh_tree()

        ttk.Button(frm, text="Check Out Selected", command=do_checkout).pack(pady=6)

    def _checkout_by_id(self, cid):
        for i, g in enumerate(self.guests):
            if g["id"] == cid:
                rn = g["room"]
                # make sure room exists before modifying
                if rn in self.rooms:
                    self.rooms[rn]["status"] = "Available"
                    self.rooms[rn]["guest_id"] = None
                removed = self.guests.pop(i)
                messagebox.showinfo("Checked out", f"{removed['name']} has been checked out from room {rn}.")
                self._refresh_availability()
                return
        messagebox.showerror("Not found", "Customer not found.")

    def show_check_out(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Check Out", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        tree = ttk.Treeview(frm, columns=("name", "room", "phone"), show="headings")
        tree.heading("name", text="Name")
        tree.heading("room", text="Room")
        tree.heading("phone", text="Phone")
        tree.pack(fill="both", expand=True, pady=8)

        def refresh():
            for r in tree.get_children():
                tree.delete(r)
            for g in self.guests:
                tree.insert("", tk.END, iid=str(g["id"]), values=(g["name"], f"{g['room']} ({g['room_type']})", g["phone"]))

        refresh()

        def checkout_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("No selection", "Please select a guest to check out.")
                return
            cid = int(sel[0])
            self._checkout_by_id(cid)
            refresh()

        ttk.Button(frm, text="Check Out Selected", command=checkout_selected).pack()

    def show_pickup_service(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Pickup Service - Schedule", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        pname = tk.StringVar()
        ptime = tk.StringVar(value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

        ttk.Label(frm, text="Guest Name:").pack(anchor="w", pady=(8, 0))
        ttk.Entry(frm, textvariable=pname).pack(fill="x")

        ttk.Label(frm, text="Pickup Time (YYYY-MM-DD HH:MM):").pack(anchor="w", pady=(8, 0))
        ttk.Entry(frm, textvariable=ptime).pack(fill="x")

        def schedule():
            name = pname.get().strip()
            tstr = ptime.get().strip()
            if not name or not tstr:
                messagebox.showwarning("Missing data", "Please provide both name and time.")
                return
            try:
                ts = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M')
            except Exception:
                messagebox.showerror("Invalid time", "Please use format YYYY-MM-DD HH:MM")
                return
            self.pickups.append({"name": name, "time": ts})
            messagebox.showinfo("Scheduled", f"Pickup scheduled for {name} at {ts}.")
            pname.set("")
            ptime.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

        ttk.Button(frm, text="Schedule Pickup", command=schedule).pack(pady=10)

    def show_update_room_status(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Update Room Status", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        tree = ttk.Treeview(frm, columns=("type", "status", "guest"), show="headings")
        tree.heading("type", text="Type")
        tree.heading("status", text="Status")
        tree.heading("guest", text="Guest ID")
        tree.pack(fill="both", expand=True, pady=8)

        def refresh():
            for r in tree.get_children():
                tree.delete(r)
            for rn, info in sorted(self.rooms.items()):
                tree.insert("", tk.END, iid=str(rn), values=(info["type"], info["status"], str(info.get("guest_id") or "-")))
        refresh()

        def toggle_status():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Select room", "Please select a room to update.")
                return
            rn = int(sel[0])
            info = self.rooms.get(rn)
            if not info:
                messagebox.showerror("Error", "Room not found.")
                return
            if info["status"] == "Occupied":
                messagebox.showwarning("Occupied", "Room is occupied. Check out the guest before changing status.")
                return
            # toggle between Available and Maintenance
            new_status = "Maintenance" if info["status"] == "Available" else "Available"
            self.rooms[rn]["status"] = new_status
            messagebox.showinfo("Updated", f"Room {rn} status set to {new_status}.")
            refresh()

        ttk.Button(frm, text="Toggle Available/Maintenance", command=toggle_status).pack()

    def show_pickup_info(self):
        self._clear_page()
        frm = tk.Frame(self.page_container, bg="#2b2b2b")
        frm.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(frm, text="Scheduled Pickups", bg="#2b2b2b", fg="#fff",
                 font=("Helvetica", 14, "bold")).pack(anchor="w")

        tree = ttk.Treeview(frm, columns=("name", "time"), show="headings")
        tree.heading("name", text="Name")
        tree.heading("time", text="Time")
        tree.pack(fill="both", expand=True, pady=8)

        def refresh2():
            for r in tree.get_children():
                tree.delete(r)
            for i, p in enumerate(sorted(self.pickups, key=lambda x: x["time"])):
                tree.insert("", tk.END, iid=str(i), values=(p["name"], p["time"].strftime('%Y-%m-%d %H:%M')))
        refresh2()

        def remove_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("No selection", "Select a pickup to remove.")
                return
            iid = int(sel[0])
            if 0 <= iid < len(self.pickups):
                removed = self.pickups.pop(iid)
                messagebox.showinfo("Removed", f"Pickup for {removed['name']} removed.")
                refresh2()
            else:
                messagebox.showerror("Error", "Selected pickup not found.")

        ttk.Button(frm, text="Remove Selected Pickup", command=remove_selected).pack(pady=6)
    def _on_close(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()


if __name__ == "__main__":
    app = HotelManagementSystem()
    app.protocol("WM_DELETE_WINDOW", app._on_close)
    app.mainloop()
