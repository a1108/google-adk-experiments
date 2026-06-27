from google.genai import types


def start_console(runner, session):
    """
    Start the interactive console.
    """

    print("\nWeather Agent Started\n")

    while True:

        question = input("You : ")

        if question.lower() == "exit":
            print("\nGoodbye!\n")
            break

        user_message = types.Content(
            role="user",
            parts=[
                types.Part(text=question)
            ],
        )

        events = runner.run(
            user_id=session.user_id,
            session_id=session.id,
            new_message=user_message,
        )

        for event in events:

            if (
                event.content
                and event.content.parts
                and event.content.parts[0].text
            ):
                print(f"\nAgent : {event.content.parts[0].text}\n")