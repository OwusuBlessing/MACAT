from src.macat.bot import refine_transcription


ts = "Welcome everybody today I will be teaching about AI and machine learning, I would love everyone of us to listen attentively and ask questions where necessary, just follow my flow."
role = "format"
res = refine_transcription(ts,role)


print(res)