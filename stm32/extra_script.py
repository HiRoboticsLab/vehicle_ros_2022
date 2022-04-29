Import("env")

# Custom HEX from ELF
env.AddPostAction(
    "$BUILD_DIR/${PROGNAME}.elf",
    env.VerboseAction(" ".join([
        "$OBJCOPY", "-O", "ihex", "-R", ".eeprom",
        "$BUILD_DIR/${PROGNAME}.elf", "$BUILD_DIR/${PROGNAME}.hex"
    ]), "Building $BUILD_DIR/${PROGNAME}.hex")
)

# from os.path import join
# # platform = env.PioPlatform()
# board = env.BoardConfig()

# # def __configure_upload_port(env):
# #     return env.subst("$UPLOAD_PORT")

# env.Replace(
#     # __configure_upload_port=__configure_upload_port,
#     # UPLOADER=join(
#     #         '"%s"' % platform.get_package_dir("tool-stm32duino") or "",
#     #         "stm32flash", "stm32flash"),
#     UPLOADERFLAGS=[
#         "-g", board.get("upload.offset_address", "0x08000000"),
#         "-R", 
#         "-i", "-rts,-dtr,dtr,-dtr:rts,-rts,dtr,rts",
#         "-b", "115200", "-w"
#     ],
#     # UPLOADCMD='$UPLOADER $UPLOADERFLAGS "$SOURCE" "${__configure_upload_port(__env__)}"'
# )

# # upload_actions = [
# #     env.VerboseAction(env.AutodetectUploadPort, "Looking for upload port..."),
# #     env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
# # ]