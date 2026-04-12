doctors = {
    "cardiology": [{"name": "Dr. Varun Kolambekar", "days": ["Monday", "Wednesday", "Friday"]}],
    "general":    [{"name": "Dr. Shraddha Kapoor",  "days": ["Monday", "Tuesday", "Wednesday"]}],
}

time_slots = ["Morning (9 AM)", "Noon (12 PM)", "Evening (5 PM)"]

faqs = {
    "visiting hours": "Visiting hours are 9 AM - 12 PM and 4 PM - 7 PM daily.",
    "timing":         "OPD timings are Monday to Saturday, 8 AM - 8 PM. Emergency is open 24/7.",
    "insurance":      "We accept most major insurance providers. Bring your insurance card and ID at admission.",
    "billing":        "Billing is at the ground floor counter. We accept cash, UPI, and all major cards.",
    "lab reports":    "Lab reports are ready within 6-24 hours. Collect at the lab counter or ask at reception.",
    "cancellation":   "To cancel, call +91 20 1234 5678 at least 2 hours before your slot.",
}

vaccines = {
    "flu":       "Flu vaccine recommended once a year, ideally before monsoon season.",
    "hepatitis": "Hepatitis B given in 3 doses over 6 months. Available at our vaccination centre.",
    "typhoid":   "Typhoid vaccine is a single injection. Booster needed every 3 years.",
    "tetanus":   "Tetanus (TT) injection available at OPD. Recommended after any deep wound.",
}

health_tips = [
    "Drink at least 8 glasses of water every day.",
    "A 30-minute walk daily can significantly improve heart health.",
    "Eat more fruits and vegetables - aim for 5 servings a day.",
    "Adults need 7-8 hours of sleep each night.",
    "Practice deep breathing or meditation to reduce stress.",
    "Avoid smoking - it is the leading cause of preventable disease.",
    "Get a routine health check-up at least once a year.",
    "Limit sugar intake to reduce the risk of diabetes and obesity.",
]

tip_index = [0]

# ── BOOKING STATE ──────────────────────────
booking_state = {}

def reset_booking(session):
    booking_state[session] = {"step": None, "dept": None, "doctor": None, "day": None}

def pick_index(msg, items):
    # items is a list of strings or dicts
    if msg.strip().isdigit():
        idx = int(msg.strip()) - 1
        if 0 <= idx < len(items):
            return items[idx]
    else:
        for item in items:
            label = item["name"] if isinstance(item, dict) else item
            if label.lower() in msg or msg in label.lower():
                return item
    return None

# ── BOOKING FLOW ───────────────────────────

def handle_booking(msg, session):
    if session not in booking_state:
        reset_booking(session)
    state = booking_state[session]
    step  = state["step"]

    # STEP 1 - show departments
    if step is None:
        state["step"] = "choose_dept"
        dept_list = "\n".join(f"  {i+1}. {d.capitalize()}" for i, d in enumerate(doctors.keys()))
        return "Let us book your appointment.\n\nChoose a specialization:\n" + dept_list + "\n\nType the name or number."

    # STEP 2 - pick department
    if step == "choose_dept":
        dept_keys = list(doctors.keys())
        chosen = pick_index(msg, dept_keys)
        if not chosen:
            return "Please type a specialization name or number from the list."
        state["dept"] = chosen
        state["step"] = "choose_doctor"
        doc_list = "\n".join(f"  {i+1}. {d['name']} ({', '.join(d['days'])})" for i, d in enumerate(doctors[chosen]))
        return "Doctors in " + chosen.capitalize() + ":\n" + doc_list + "\n\nType the doctor's name or number."

    # STEP 3 - pick doctor
    if step == "choose_doctor":
        dept     = state["dept"]
        doc_list = doctors[dept]
        chosen   = pick_index(msg, doc_list)   # returns a dict
        if not chosen:
            return "Please type the doctor's name or number from the list."
        state["doctor"] = chosen["name"]
        state["step"]   = "choose_day"
        days     = chosen["days"]
        day_list = "\n".join(f"  {i+1}. {d}" for i, d in enumerate(days))
        return chosen["name"] + " is available on:\n" + day_list + "\n\nWhich day works for you?"

    # STEP 4 - pick day
    if step == "choose_day":
        dept     = state["dept"]
        doc_name = state["doctor"]
        doc      = next(d for d in doctors[dept] if d["name"] == doc_name)
        days     = doc["days"]
        chosen   = pick_index(msg, days)
        if not chosen:
            return "Please choose a valid day from the list above."
        state["day"]  = chosen
        state["step"] = "choose_slot"
        slot_list = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(time_slots))
        return "Available slots on " + chosen + ":\n" + slot_list + "\n\nWhich time do you prefer?"

    # STEP 5 - pick slot and confirm
    if step == "choose_slot":
        chosen = pick_index(msg, time_slots)
        if not chosen:
            return "Please choose a valid time slot from the list above."
        doc = state["doctor"]
        dept = state["dept"].capitalize()
        day = state["day"]

        from database import is_slot_taken, save_appointment
        if is_slot_taken(doc, day, chosen):
            slot_list = "\n".join(f"  {i + 1}. {s}" for i, s in enumerate(time_slots))
            return ("Sorry, " + chosen + " with " + doc + " on " + day + " is already booked.\n\n"
                    "Please choose another slot:\n" + slot_list)

        save_appointment(doc, dept, day, chosen)
        reset_booking(session)
        return ("Appointment Confirmed!\n\n"
                "  Department : " + dept + "\n"
                "  Doctor     : " + doc + "\n"
                "  Day        : " + day + "\n"
                "  Time       : " + chosen + "\n\n"
                "Please arrive 10 minutes early with a valid ID.\n"
                "For changes, call +91 20 1234 5678.")

    reset_booking(session)
    return "Something went wrong. Type 'book appointment' to start again."


# ── MAIN RESPONSE FUNCTION ─────────────────

def get_response(user_message, session="default"):
    msg = user_message.lower().strip()

    # keep user in booking flow if active
    if booking_state.get(session, {}).get("step") is not None:
        return handle_booking(msg, session)

    # GREETING
    if any(w in msg for w in ["hi", "hello", "hey", "good morning", "good evening"]):
        return ("Hello! Welcome to MiniProject Hospital. I am MediBot.\n\n"
                "I can help you with:\n"
                "- Book an appointment\n"
                "- Find a doctor\n"
                "- Health tips\n"
                "- Vaccines\n"
                "- Billing, insurance, lab reports")

    # APPOINTMENT
    if any(w in msg for w in ["appointment", "book", "schedule", "consult"]):
        return handle_booking(msg, session)

    # DOCTOR SEARCH
    if any(w in msg for w in ["doctor", "specialist", "find", "cardio", "general"]):
        if any(w in msg for w in ["heart", "cardio"]):
            key = "cardiology"
        elif any(w in msg for w in ["general", "fever", "cold"]):
            key = "general"
        else:
            return "We have: " + ", ".join(d.capitalize() for d in doctors.keys()) + "\nWhich department?"
        result = key.capitalize() + " Doctors:\n"
        for d in doctors[key]:
            result += "  - " + d["name"] + " (" + ", ".join(d["days"]) + ")\n"
        return result + "\nType 'book appointment' to schedule."

    # HEALTH TIPS
    if any(w in msg for w in ["tip", "advice", "healthy", "wellness"]):
        tip = health_tips[tip_index[0] % len(health_tips)]
        tip_index[0] += 1
        return "Health Tip: " + tip

    # VACCINES
    if any(w in msg for w in ["vaccine", "vaccination", "flu", "hepatitis", "typhoid", "tetanus"]):
        for vac, info in vaccines.items():
            if vac in msg:
                return vac.capitalize() + " Vaccine: " + info + "\n\nVaccination Centre - 1st floor."
        return "We provide: " + ", ".join(v.capitalize() for v in vaccines.keys()) + "\nAsk about any specific one!"

    # INSURANCE
    if any(w in msg for w in ["insurance", "cashless", "claim"]):
        return faqs["insurance"]

    # BILLING
    if any(w in msg for w in ["bill", "payment", "pay", "fees", "cost"]):
        return faqs["billing"]

    # CANCELLATION
    if any(w in msg for w in ["cancel", "reschedule"]):
        return faqs["cancellation"]

    # LAB
    if any(w in msg for w in ["lab", "test", "report", "blood", "urine"]):
        return faqs["lab reports"] + "\nLab open Mon-Sat, 7 AM - 6 PM."

    # TIMING
    if any(w in msg for w in ["timing", "hours", "open", "opd"]):
        return faqs["timing"]

    # VISITING
    if "visiting" in msg:
        return faqs["visiting hours"]

    # EMERGENCY
    if any(w in msg for w in ["emergency", "ambulance", "urgent"]):
        return "Call 108 immediately!\nHospital ambulance: +91 20 1234 5678\nEmergency open 24/7."

    # GOODBYE
    if any(w in msg for w in ["bye", "thanks", "thank you", "done"]):
        return "Thank you! Stay healthy. Take care!"

    # FALLBACK
    return ("I did not understand that.\n"
            "I can help with: appointments, doctors, vaccines, health tips, billing, insurance, lab reports.")


# # ── TERMINAL TEST ──────────────────────────
# if __name__ == "__main__":
#     print("MediBot running. Type 'bye' to exit.\n")
#     while True:
#         user_input = input("You: ")
#         if not user_input.strip():
#             continue
#         print("MediBot: " + get_response(user_input) + "\n")
#         if "bye" in user_input.lower():
#             break
