# initialize flask app
import os
import re
import time
from flask import Flask, Response, json, request, jsonify;
from openai import OpenAI
import requests
from flask_cors import CORS
from db import Major, db
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devilspathway.db'
app.config['SQLALCHEMY_POOL_SIZE'] = 30
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30

# initialize db connection
db.init_app(app)
with app.app_context():
    db.create_all()

gpt_initial_prompt_v1 = "Create a 'Choose Your Own Adventure' style interaction to infer a user's top 3 RIASEC personality types.\
Use a series of 6 chapters, each offering 4 distinct choices, \
to guide the user through a narrative. Each chapter should be sent separately.\
You have to wait for the user to respond with their choice before you move on with \
the next chapter. After the final choice, provide an analysis of their top 3 RIASEC types based on their selections. \
Format for chapters in JSON: Each chapter should be sent as JSON data containing: chapterNumber: (number) The chapter number. \
chapterTitle: (string) Title of the chapter. chapterDescription: (string) Description \
of the scenario or situation.chapterOptions: (array) An array of objects representing the \
available choices. Each object should contain:optionNumber: (number) The number associated with the choice. \
optionDescription: (string) Description of the choice.The user will respond with a single number (1-4) indicating their choice, everytime you send a chapter. \
Please wait for each one of those before sending the second chapter or the perosnality types. After the user responds to chapter 6, provide the analysis as JSON data containing an array named personalities that has objects \
representing their top 3 RIASEC personality types. Each object should contain: name: (string) The name of the personality type (e.g., Enterprising (E)). \
description: (string) A brief description of the personality type based on the user's choices. \
You responses should only be in JSON. Stick to this format and avoid adding any additional text. Make sure to send each chapter at a time"


gpt_initial_prompt_before_interest = "Create a 'Choose Your Own Adventure' style interaction to infer a user's top 3 RIASEC personality types and top 3 work values. Your work value options are recognition, achievement, working conditions, relationships, independence, and support. Individuals that value achievement are results oriented and like to use their strongest abilities to get a feeling of accomplishment. Individuals that value independence enjoy working on their own and making decisions. Individuals that value recognition like to receive acknowledgement and praise from others, and they enjoy opportunities for leadership and career advancement. Individuals that value relationships appreciate opportunities to provide service to others and work with co-workers in a friendly non-competitive environment. Individuals that value support want to be surrounded by individuals that will guide them, provide resources, and ensure their wellbeing. Individuals that value working conditions want job security, low health risks, and good compensation for their efforts. Use a series of 8 chapters, each offering 4 distinct choices, to guide the user through fictional scenarios with plot, theme, setting, and character, with a tone of adventure and mystery. Each chapter scenario should be brief; do not go over 75 words. The chapter scenario should be specific enough for the user to imagine it. The answer choices should be composed of a single short sentence. Your narrative should very subtly incorporate my interests which are: "  

gpt_initial_prompt_after_interest = " .You have to wait for the user to respond with their choice before you move on with the next chapter. After the eight chapters and eight user responses, provide an analysis of their top 3 RIASEC types and top 3 work values based on their selections. Format for chapters in JSON: Each chapter should be sent as JSON data containing: chapterNumber: (number) The chapter number.  chapterTitle: (string) Title of the chapter. chapterDescription: (string) Description of the scenario or situation chapterOptions: (array) An array of objects representing the available choices. Each object should contain: optionNumber: (number) The number associated with the choice.  optionDescription: (string) Description of the choice. The user will respond with a single number (1-4) indicating their choice, everytime you send a chapter. Please wait for each one of those before sending the second chapter or the personality types. After the user responds to chapter 8, provide the analysis as JSON data containing an array named 'personalities' that has objects representing their top 3 RIASEC personality types and an array named 'work_values' that has objects representing their top 3 work values. Each personality object should contain: 'name': (string) The name of the personality type (e.g., Enterprising (E)). 'description': (string) A brief description of the personality type based on the user's choices. Each work_value object should contain: 'name': (string) The name of the work value (e.g., Recognition)) 'description': (string) A brief description of the work value based on the user's choices. Your responses should only be in JSON. Avoid adding spaces in the JSON keys. Stick to this format and avoid adding any additional text. Make sure to send each chapter at a time."

gpt_career_prompt = "Based on my top 3 RIASEC personality type, my major, \
    and my hobby that I will give you, and your job is to suggest careers that align with those. \
        You will retrieve these careers from the file attached in your retrival tool. \
        The careers should be in the my major domain.\
        Format the response as an array in JSON:In each object, please include careerName, \
            description (why do you think it is a match based on RIASEC), \
        careerCode ( this wil be ONET code). The careers should be only taken form the occupations file attached."

gpt_career_prompt_pt1 = "Generate a JSON-formatted list of the top six careers tailored to my provided academic major, RIASEC personality type (R-Realistic, I-Investigative, A-Artistic, S-Social, E-Enterprising, C-Conventional), work values, personal interests, and skills, prioritizing in that order. For each career, include. Overall the output will have an array of 6 objects, each containing: career_name (string), career_rationale (string) [ description detailing the rationale behind its match. Focus on how it aligns with the major, RIASEC personality type (mentioning only those aspects of the RIASEC that match my profile), work values, interests, and/or skills. Please ensure rationales do not include RIASEC dimensions that are not part of my specified profile. For example, if the user’s profile is SIA, only include RIASEC dimensions that are social, investigative, or artistic in the rationale.], career_description(string) [A brief overview of the role and its responsibilities.], essential_duties (array of strings) [this will be a list of 3 essential duties for that career], work_style (array of strings) [personality trait or work style typical for the career]), average_salary(number)[this will be the average yearly salary of this job in the US]. Note: The academic major, RIASEC personality type, work values, personal interests, and skills will be provided as inputs for each query. Please only provide the JSON-formatted list, not any additional information."

gpt_career_prompt_pt2 = "Refer exclusively to the 'careers.json' file to identify similar jobs for each career suggestion provided. For each initial career path suggested, append a list of ‘related jobs’ that are directly found within the 'careers.json' file. Each 'related job' must include its career title (“Title”) and career code (“O*NET-SOC Code”). It is crucial to verify the presence of each related job in the “careers.json” file before including them in your response, and to ensure that careers are grouped or separated exactly as they are in the file, without making assumptions about their similarities or differences based on external knowledge. Please format your response in JSON as an array of 6 objects, with each object structured as follows: career_name (string): The name of the initial career path suggested. related_jobs (array of objects): An array of similar jobs extracted from the 'careers.json' file, with each job represented by two properties—career_title (string) and career_code (string). Please provide the JSON response without any special markers or annotations, just the raw data."

gpt_career_prompt_pt3 = "Using only the data from the 'asu-classes.json' file I've uploaded, identify courses directly relevant to the six careers you suggested. Ensure each selected course strictly corresponds with the career it's matched to, considering the career's typical responsibilities and required knowledge areas. Additionally, cross-reference with the 'CertificatesMinors.json' file to suggest relevant certificates or minors for these careers. Confirm the existence of each certificate/minor in their respective files before listing them in your response. Please format your response as a JSON array with 6 objects, corresponding to each career. For each object, include: `career_name`: String, specifying the career classes`: Array of objects, where each object contains: `class_name`: String, taken from the COURSETITLELONG field in 'asu-classes.json'; `class_code`: String, combining the SUBJECT and CATALOGNBR fields from 'asu-classes.json'.`asu_certs`: Array of objects, with each object detailing: `cert_name`: String, from the “Programs” column in 'CertificatesMinors.json'; and `cert_link`: String, URL from its corresponding “Link” column in 'CertificatesMinors.json'."

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return "hello";


@app.route('/gpt-riasec', methods=['POST'])
def chatwithGPT():
    my_messages = []
    data = request.json
    step_number = data.get('step_number')
    if step_number is 0:
        interests= data.get('interests')
        my_messages = [{"role": "system",  "content": gpt_initial_prompt_before_interest + interests + gpt_initial_prompt_after_interest}]
    else:
        my_messages = data.get('messages', [])
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    response_format = {"type": "json_object" },
    messages= my_messages,
    n=1)
    content = completion.choices[0].message.content
    # json_content = json.loads(content)
    my_messages = append_to_messages(my_messages, "assistant", content)
    return jsonify(my_messages)

@app.route('/gpt-career', methods=['POST'])
def careerwithGPT():
    data = request.json
    student_interests = data.get('student_interests')
    student_skills = data.get('student_skills')
    student_major = data.get('student_major')
    student_riasec = data.get('student_riasec')
    combined_sentence = f"My major is {student_major}, my RIASEC code is {student_riasec}, my skills are {student_skills} and my interests are {student_interests}."
    response = ''
    client = OpenAI(api_key=os.environ.get('z_api_key'))
    assistant_id="asst_1xAUhFkBivJyvdBvBXHGHIBs"
    thread = client.beta.threads.create()
    response1 = ""
    response2 = ""
    response3 = ""
    #### Pre-Message ####
    hello_thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= "hello, please my respond to my next message")
    hello_run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id)
    while hello_run.status in ["queued", "in_progress"]:
        keep_retrieving_run_hello = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=hello_run.id
        )
        if keep_retrieving_run_hello.status == "completed":
            # Step 7: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message_hello_id = all_messages.first_id
            message_hello = client.beta.threads.messages.retrieve(
                 message_id=message_hello_id,
                 thread_id=thread.id
                 )
            response_hello = message_hello.content[0].text.value
            break
        elif keep_retrieving_run_hello.status == "queued" or keep_retrieving_run_hello.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run_hello.status}")
            break
    print(response_hello)

    ###### First Message ######
    first_thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= gpt_career_prompt_pt1 + combined_sentence)
    first_run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id)
    while first_run.status in ["queued", "in_progress"]:
        keep_retrieving_run1 = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=first_run.id
        )
        if keep_retrieving_run1.status == "completed":
            # Step 7: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message1_id = all_messages.first_id
            message1 = client.beta.threads.messages.retrieve(
                 message_id=message1_id,
                 thread_id=thread.id
                 )
            response1 = message1.content[0].text.value
            break
        elif keep_retrieving_run1.status == "queued" or keep_retrieving_run1.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run1.status}")
            break
    # Use regular expression to find the JSON string
    match = re.search(r"```json\n(.+?)\n```", response1, re.DOTALL)
    if match:
        json_string = match.group(1)  # Extract the JSON string
        response1 = json.loads(json_string)  # Parse the JSON string into a Python object
        print("match1:" + json_string)
    else:
        print("No JSON string found.")
        print("no match:" + response1)

    #### Pre-Message ####
    thank_thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= "Thank you, please respond to my next message")
    hello_run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id)
    while hello_run.status in ["queued", "in_progress"]:
        keep_retrieving_run_hello = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=hello_run.id
        )
        if keep_retrieving_run_hello.status == "completed":
            # Step 7: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message_hello_id = all_messages.first_id
            message_hello = client.beta.threads.messages.retrieve(
                 message_id=message_hello_id,
                 thread_id=thread.id
                 )
            response_hello = message_hello.content[0].text.value
            break
        elif keep_retrieving_run_hello.status == "queued" or keep_retrieving_run_hello.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run_hello.status}")
            break
    print(response_hello)


    ######## second message #######

    second_thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= gpt_career_prompt_pt2,
        file_ids=["file-ElmMtbh8l48rGIF9S5RwVmg4"])
    second_run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id)
    while second_run.status in ["queued", "in_progress"]:
        keep_retrieving_run2 = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=second_run.id
        )
        if keep_retrieving_run2.status == "completed":
            # Step 7: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message2_id = all_messages.first_id
            message2 = client.beta.threads.messages.retrieve(
                 message_id=message2_id,
                 thread_id=thread.id
                 )
            response2 = message2.content[0].text.value
            break
        elif keep_retrieving_run2.status == "queued" or keep_retrieving_run2.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run2.status}")
            break
    # Use regular expression to find the JSON string
    match = re.search(r"```json\n(.+?)\n```", response2, re.DOTALL)
    if match:
        json_string = match.group(1)  # Extract the JSON string
        response2 = json.loads(json_string)  # Parse the JSON string into a Python object
        print("match2:" + json_string)
    else:
        print("No JSON string found.")
        print("no match:" + response2)

   #### Pre-Message ####
    thank_thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= "Thank you, please respond to my next message")
    hello_run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id)
    while hello_run.status in ["queued", "in_progress"]:
        keep_retrieving_run_hello = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=hello_run.id
        )
        if keep_retrieving_run_hello.status == "completed":
            # Step 7: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message_hello_id = all_messages.first_id
            message_hello = client.beta.threads.messages.retrieve(
                 message_id=message_hello_id,
                 thread_id=thread.id
                 )
            response_hello = message_hello.content[0].text.value
            break
        elif keep_retrieving_run_hello.status == "queued" or keep_retrieving_run_hello.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run_hello.status}")
            break
    print(response_hello)


      ######## Third message #######
        
    third_thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=gpt_career_prompt_pt3,
        file_ids=["file-IdyAT054U5ghvYyUwYgWgX2d", "file-LaJe7q29tXfOUKuQMIzWrPxn"])
    third_run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id)
    while third_run.status in ["queued", "in_progress"]:
        keep_retrieving_run3 = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=third_run.id
        )
        if keep_retrieving_run3.status == "completed":
            # Step 7: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            message3_id = all_messages.first_id
            message3 = client.beta.threads.messages.retrieve(
                 message_id=message3_id,
                 thread_id=thread.id
                 )
            response3 = message3.content[0].text.value
            break
        elif keep_retrieving_run3.status == "queued" or keep_retrieving_run3.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run3.status}")
            break
    # Use regular expression to find the JSON string
    match = re.search(r"```json\n(.+?)\n```", response3, re.DOTALL)
    if match:
        json_string = match.group(1)  # Extract the JSON string
        response3 = json.loads(json_string)  # Parse the JSON string into a Python object
        print("match3:" + json_string)
    else:
        print("No JSON string found.")
        print("no match:" + response3)

    final_response = combine_json(response1, response2, response3)
    return jsonify(final_response)


@app.route('/majors', methods=['GET'])
def get_majors():
    majors_query = Major.query.with_entities(Major.name).all()
    majors_list = [name[0] for name in majors_query]  # Unpack each name from the result tuples
    return jsonify(majors_list)


@app.route('/onet/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Construct the URL to the external API
    external_url = f'https://services.onetcenter.org/ws/mnm/{path}'

    # Extract headers from the incoming request
    # Add or modify headers as needed, particularly for authentication
    headers = {
        'Authorization': 'SECRET SECRET',
        'Accept': 'application/json' 
    }

    # Forward the request to the external API
    if request.method == 'GET':
        response = requests.get(external_url, headers=headers, params=request.args)
    elif request.method == 'POST':
        response = requests.post(external_url, headers=headers, json=request.json)
    elif request.method == 'PUT':
        response = requests.put(external_url, headers=headers, json=request.json)
    elif request.method == 'DELETE':
        response = requests.delete(external_url, headers=headers)
    else:
        return jsonify({'error': 'Method not supported'}), 405

     # Exclude headers that can cause trouble.
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    # Create the response to send back to the client.
    response = Response(response.content, response.status_code, headers)
    return response



def append_to_messages(messages, user, content):
    """
    Append a new message to the "messages" array.

    Args:
    - messages (list): The existing list of messages.
    - user (str): The user who sent the message.
    - content (str): The content of the message.

    Returns:
    - list: The updated list of messages.
    """
    new_message = {"role": user, "content": content}
    messages.append(new_message)
    return messages


def combine_json(json1, json2, json3):
    # Create a dictionary from JSON2 and JSON3 for quick lookup based on career_name
    json2_dict = {item["career_name"]: item["related_jobs"] for item in json2}
    json3_dict = {item["career_name"]: {"classes": item["classes"], "asu_certs": item["asu_certs"]} for item in json3}

    # Iterate through JSON1 and enrich it with data from JSON2 and JSON3 based on career_name
    for item in json1:
        career_name = item["career_name"]
        
        # Add related_jobs from JSON2 if available
        if career_name in json2_dict:
            item["related_jobs"] = json2_dict[career_name]
        
        # Add classes and asu_certs from JSON3 if available
        if career_name in json3_dict:
            item.update(json3_dict[career_name])
    
    return json1


# Release resources in case the app crashes
@app.teardown_appcontext
def teardown_context(exception=None):
    db.session.connection().close()

if __name__ == "__main__":
    print("Starting Flask server")
    app.run(host='0.0.0.0', port=5000, debug=False)
