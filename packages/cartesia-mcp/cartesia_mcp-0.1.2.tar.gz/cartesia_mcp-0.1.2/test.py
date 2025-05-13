    # try:
    #     voices = list_voices()
    #     id = voices[0].id

    #     # print(update_voice(id, "Test Update Name", "Test Update Description"))
    #     print(get_voice(id))

    #     tts = text_to_speech("Hello, world!", {"mode": "id", "id": id}, {
    #         "container": "mp3",
    #         "sample_rate": 44100,
    #         "bit_rate": 192000
    #     })

    #     clone = clone_voice(tts["file_path"], "test", "en", "similarity")
    #     print("CLONE ", clone)

    #     localize = localize_voice(clone.id, "test", "test", "en", "male")
    #     print("LOCALIZE ", localize)

    #     print(
    #         "CHANGE ",
    #         voice_change(
    #             file_path=tts["file_path"],
    #             voice_id=voices[1].id,
    #             output_format_container="mp3",
    #             output_format_sample_rate=44100,
    #             output_format_bit_rate=192000))

    #     print(
    #         "INFILL ",
    #         infill(
    #             transcript="Hello, world!",
    #             language="en",
    #             voice_id=voices[1].id,
    #             left_audio_file_path=tts["file_path"],
    #             output_format_container="mp3",
    #             output_format_sample_rate=44100,
    #             output_format_bit_rate=192000))
    # except Exception as e:
    #     print(e)