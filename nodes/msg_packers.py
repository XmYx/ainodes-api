
import base64
import io

import msgpack



def create_pack(image, node_id):
    buffer = io.BytesIO()

    image.save(buffer, format="JPEG")
    json_msg = {"id": node_id,
                "image": base64.b64encode(buffer.getvalue()).decode()}
    pack = msgpack.packb(json_msg)
    return pack

