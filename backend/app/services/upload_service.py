import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from typing import List
import uuid

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

class UploadService:
    @staticmethod
    async def upload_image(file: UploadFile, folder: str = "kutubxona") -> str:
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}"
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file.file,
                folder=folder,
                public_id=filename,
                resource_type="image",
                format="webp",
                quality="auto",
                fetch_format="auto"
            )
            
            return result["secure_url"]
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload image: {str(e)}"
            )
    
    @staticmethod
    async def upload_multiple_images(files: List[UploadFile], folder: str = "kutubxona") -> List[str]:
        if len(files) > 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 8 images allowed"
            )
        
        urls = []
        for file in files:
            url = await UploadService.upload_image(file, folder)
            urls.append(url)
        
        return urls
    
    @staticmethod
    async def delete_image(public_id: str):
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete image: {str(e)}"
            )
