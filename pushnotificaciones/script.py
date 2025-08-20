# generate_vapid_keys.py
# pip install py-vapid cryptography
#
# from py_vapid import Vapid
# import json
# import base64
# from cryptography.hazmat.primitives import serialization
#
# # Generar llaves VAPID
# vapid = Vapid()
# vapid.generate_keys()
#
# # Serializar claves en formato DER (binario)
# public_key_der = vapid.public_key.public_bytes(
#     encoding=serialization.Encoding.X962,
#     format=serialization.PublicFormat.UncompressedPoint
# )
#
# private_key_der = vapid.private_key.private_bytes(
#     encoding=serialization.Encoding.DER,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption()
# )
#
# # Convertir a Base64 URL-safe (lo que espera Web Push)
# public_key_b64 = base64.urlsafe_b64encode(public_key_der).decode("utf-8")
# private_key_b64 = base64.urlsafe_b64encode(private_key_der).decode("utf-8")
#
# print("=== LLAVES VAPID GENERADAS ===")
# print(f"PUBLIC_KEY: {public_key_b64}")
# print(f"PRIVATE_KEY: {private_key_b64}")
#
# # Guardar en archivo JSON
# keys_data = {
#     "public_key": public_key_b64,
#     "private_key": private_key_b64
# }
#
# with open("../vapid_keys.json", "w") as f:
#     json.dump(keys_data, f, indent=2)
#
# # Guardar clave privada en formato PEM (útil para Django backend)
# with open("../private_key.pem", "wb") as f:
#     f.write(
#         vapid.private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption()
#         )
#     )
#
# print("\nLlaves guardadas en:")
# print("- vapid_keys.json (para settings.py)")
# print("- private_key.pem (archivo PEM)")
# print("\nUSO:")
# print("- PUBLIC_KEY: Angular frontend (suscripción)")
# print("- PRIVATE_KEY: Django backend (envío notificaciones)")
#

from py_vapid import Vapid01

vapid = Vapid01.from_file("../../private_key.pem")
print(vapid.public_key())
