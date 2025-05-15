# basic import 
from mcp.server.fastmcp import FastMCP  
import math
import mcp.types as types
from rdkit import Chem
from rdkit.Chem import Draw
import base64
from rdkit.Chem import Descriptors
import pandas
import requests
import json


# instantiate an MCP server client
mcp = FastMCP("rdkit-mcp-server")

# DEFINE TOOLS


import io
def pil_image_to_base64(img, format="PNG"):
    """
    Converts a PIL Image object to a base64 string.

    Args:
        img: PIL Image object.
        format: Image format for saving to buffer (e.g., "PNG", "JPEG").

    Returns:
        A base64 encoded string representation of the image.
    """
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    img_byte = buffered.getvalue()
    img_str = base64.b64encode(img_byte).decode()
    return img_str

def img_byte_to_base64(img_byte):
    """
    Converts a byte array to a base64 string.

    Args:
        img_byte: Byte array of the image.

    Returns:
        A base64 encoded string representation of the image.
    """
    img_str = base64.b64encode(img_byte).decode()
    return img_str


def smiles_to_html_image(smiles: str) -> str:
    """
    Generate an HTML <img> tag with a base64-encoded PNG image from a SMILES string.

    Args:
        smiles: SMILES string of the molecule.
    Returns:
        HTML <img> tag as a string.
    """
    m = Chem.MolFromSmiles(smiles)
    img = Draw.MolToImage(m)
    img_str = pil_image_to_base64(img)
    html_img = f'<img src="data:image/png;base64,{img_str}" alt="Molecule Image" />'
    return html_img


@mcp.tool()
def smiles_to_image(smiles:str) :
    """Generate image from SMILES string"""
    m = Chem.MolFromSmiles(smiles)
    img = Draw.MolToImage(m)
    print(dir(img))
    img_str = pil_image_to_base64(img)
    response = requests.post("http://localhost:8001/upload_base64", data=json.dumps({"base64_image": img_str}))

    if response.status_code == 200:
        print(response.json())
        image_url = response.json().get("url")
        return image_url
    # return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVqK-n_XqwC9qehyBJAulLFp6U9HnhtlrUsk-9GN6iMbOlUflXWcV0Dgr5HtLyyCQ1aY0&usqp=CAU"
            
@mcp.tool()
def get_molecule_descriptors_from_smiles(smiles:str):
    m = Chem.MolFromSmiles(smiles)
    descriptors = [Descriptors.CalcMolDescriptors(m)]
    df = pandas.DataFrame(descriptors)
    print(df.head())
    table_as_string = df.to_string(index=False)
    return table_as_string

@mcp.tool()
def visualize_chemical_reaction(smart_str:str):
    """Generate image for chemical reaction from SMARTS string"""
    from rdkit.Chem import AllChem
    from rdkit.Chem import Draw
    rxn = AllChem.ReactionFromSmarts(smart_str,useSmiles=True)
    d2d = Draw.MolDraw2DCairo(800,300)
    d2d.DrawReaction(rxn)
    png = d2d.GetDrawingText()
    img_str = img_byte_to_base64(png)
    response = requests.post("http://localhost:8001/upload_base64", data=json.dumps({"base64_image": img_str}))
    if response.status_code == 200:
        print(response.json())
        image_url = response.json().get("url")
        return image_url
    

@mcp.tool()
def search_substructure(smiles:str, substructure_smiles:str,use_chirality:bool=False):
    """Search for substructure in a molecule"""
    m = Chem.MolFromSmiles(smiles)
    substructure = Chem.MolFromSmiles(substructure_smiles)
    match = m.HasSubstructMatch(substructure,useChirality=use_chirality)
    print("MATCH",match)
    is_match = None
    if match:
        is_match = True
        matches = m.GetSubstructMatches(substructure)
        return types.TextContent(
            type="text",
                    text=f"Substructure found at: str {matches}",
                )

    else:
        is_match = False
        return types.TextContent(
            type="text",
                    text=f"Substructure not found",
        )

@mcp.tool()
def get_smiles_from_name(chemical_name:str):
    """Get SMILES string from name"""
    get_smile_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/property/CanonicalSMILES/JSON"
    response = requests.get(get_smile_url)
    response_json = response.json()
    canonical_smiles = response_json["PropertyTable"]["Properties"][0].get("CanonicalSMILES","Sorry No SMILES found")
    return types.TextContent(
        type="text",
                text=f"SMILES: {canonical_smiles}",
            )

async def main():
    mcp.run("stdio")


# import fastapi
# import uvicorn
# import asyncio
# from fastapi import routing, staticfiles, FastAPI, UploadFile, HTTPException
# import base64
# import os
# from uuid import uuid4
# from pydantic import BaseModel
# app = fastapi.FastAPI(
    
#     redirect_slashes=True,
#     routes=[]
    
# )
# class Item(BaseModel):
#     base64_image: str
# @app.post("/upload_base64")
# async def upload_base64_image(item: Item):
#     try:
#         # Decode the base64 image
#         image_data = base64.b64decode(item.base64_image)
        
#         # Generate a unique filename
#         filename = f"{uuid4().hex}.png"
#         file_path = os.path.join("uploads", filename)

#         # Ensure the uploads directory exists
#         os.makedirs("uploads", exist_ok=True)

#         # Save the image to the uploads directory
#         with open(file_path, "wb") as f:
#             f.write(image_data)

#         # Return the URL for the uploaded image
#         return {"url": f"http://localhost:8001/uploads/{filename}"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

# # Serve static files from the uploads directory
# app.mount("/uploads", staticfiles.StaticFiles(directory="uploads"), name="uploads")

#  # execute and return the stdio output
# # if __name__ == "__main__":

# #     mcp.run(transport="sse")
# if __name__ == "__main__":
#     async def main():
#         # Create tasks for both servers
#         mcp_server =  mcp.run_sse_async()
        
#         http_server = asyncio.create_task(
#             asyncio.to_thread(uvicorn.run, app, host="0.0.0.0", port=8001)
#         )
#         # Wait for both tasks to complete
#         await asyncio.gather(mcp_server, http_server)
    
#     asyncio.run(main())
