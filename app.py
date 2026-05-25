from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from datetime import datetime
import random

app = Flask(__name__)

generated_proposal = ""
generated_project_title = ""

# =========================
# Home Page
# =========================
@app.route("/", methods=["GET", "POST"])
def home():

    global generated_proposal
    global generated_project_title

    proposal = ""

    if request.method == "POST":

        project_title = request.form.get("project_title")
        project_budget = request.form.get("project_budget")
        project_timeline = request.form.get("project_timeline")
        past_work = request.form.get("past_work")

        generated_project_title = project_title

        # =========================
        # Format URLs
        # =========================
        urls = past_work.split("\n")

        past_work_text = ""

        for url in urls:

            if url.strip():

                past_work_text += f"• {url.strip()}\n"

        # =========================
        # Template 1
        # =========================
        template1 = f"""Hello,

I am interested in your project "{project_title}".

With strong experience in Python development, web applications,automation, and custom business solutions, I can develop a reliable, scalable, and well-structured module as per your requirements.

Project Details:
• Budget: {project_budget}
• Estimated Timeline: {project_timeline}

I focus on clean coding standards, optimized performance, security, and timely delivery. I also provide proper communication and regular project updates throughout the development process.

You can review some of my previous work here:
{past_work_text}

I would be happy to discuss the project requirements in detail and start immediately.

Looking forward to working with you.

Best Regards,
"""

        # =========================
        # Template 2
        # =========================
        template2 = f"""Dear Client,

I would like to submit my proposal for your project "{project_title}".

I have experience in developing custom Python-based solutions, APIs, automation systems, admin panels, and scalable web applications.

I can deliver the required module with proper coding structure, documentation, and testing within the committed timeline.

Project Overview:
• Project Budget: {project_budget}
• Delivery Timeline: {project_timeline}

Why choose me?
• Professional and responsive communication
• Clean and maintainable code
• On-time delivery
• Post-development support

Past Work:
{past_work_text}

Please share the detailed scope so I can provide the best possible
solution for your project.

Thank you for your consideration.

Regards,
        """

        # =========================
        # Random Template Selection
        # =========================
        proposal = random.choice([template1, template2])

        generated_proposal = proposal

    return render_template(
        "index.html",
        proposal=proposal
    )

# =========================
# Download PDF
# =========================
@app.route("/download-pdf")
def download_pdf():

    global generated_proposal
    global generated_project_title

    if not generated_proposal:
        return "No proposal generated"

    # =========================
    # Current Date & Time
    # =========================
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # =========================
    # File Name
    # =========================
    safe_project_title = generated_project_title.replace(" ", "_")

    file_name = f"{safe_project_title}_proposal_{current_time}.pdf"

    # =========================
    # Create PDF
    # =========================
    pdf = canvas.Canvas(file_name)

    # PDF Title
    pdf.setTitle(f"{generated_project_title} Proposal")

    pdf.setFont("Helvetica", 11)

    y = 800

    lines = generated_proposal.split("\n")

    for line in lines:

        pdf.drawString(40, y, line)

        y -= 20

        # New Page
        if y < 40:

            pdf.showPage()

            pdf.setFont("Helvetica", 11)

            y = 800

    # =========================
    # Save PDF
    # =========================
    pdf.save()

    # =========================
    # Download File
    # =========================
    return send_file(
        file_name,
        as_attachment=True
    )

# =========================
# Run App
# =========================
if __name__ == "__main__":

    app.run(debug=True)