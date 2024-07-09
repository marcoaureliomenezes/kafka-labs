import faust



app = faust.App('myapp', broker='kafka://localhost:9092')

greetings_topic = app.topic('greetings', value_type=str, value_serializer='raw')

@app.agent(greetings_topic)
async def greettings_processor(stream):
    async for greeting in stream:
        print(f'Hello {greeting}!')