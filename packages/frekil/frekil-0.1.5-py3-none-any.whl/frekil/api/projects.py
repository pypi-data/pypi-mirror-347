"""
Projects API endpoints
"""

from typing import List, Dict, Any, Optional
from .base import BaseAPI


class ProjectsAPI(BaseAPI):
    """
    Projects API endpoints

    This class provides methods for interacting with the Frekil Projects API.
    """

    def list(self) -> List[Dict[str, Any]]:
        """
        List all projects the authenticated user has access to

        Returns:
            list: List of projects
        """
        return self.client.get("projects/")

    def get_membership(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get membership details for a specific project including user roles and status

        Args:
            project_id (str): The project ID

        Returns:
            list: List of project memberships
        """
        return self.client.get(f"projects/{project_id}/membership/")

    def get_images(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all images in a project

        Args:
            project_id (str): The project ID

        Returns:
            list: List of images with their metadata:
                [
                    {
                        "id": "uuid",
                        "filename": "image1.dcm",
                        "created_at": "2024-03-21T10:00:00Z",
                        "updated_at": "2024-03-21T10:00:00Z"
                    },
                    ...
                ]
        """
        return self.client.get(f"projects/{project_id}/images/")

    def get_allocations(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all allocations in a project, including user roles for both annotators and reviewers

        Args:
            project_id (str): The project ID

        Returns:
            list: List of allocations with their metadata:
                [
                    {
                        "allocation_id": "uuid",
                        "image_id": "images/image1.dcm",
                        "image_filename": "image1.dcm",
                        "annotator_id": "uuid",
                        "annotator_role": "ANNOTATOR",  # Annotator's role in the project
                        "reviewer_id": "uuid",
                        "reviewer_role": "REVIEWER",    # Reviewer's role in the project
                        "status": "PENDING",
                        "created_at": "2024-03-21T10:00:00Z",
                        "updated_at": "2024-03-21T10:00:00Z",
                        "completed_at": null
                    },
                    ...
                ]

        Note:
            - image_id is the full image key path
            - image_filename is extracted from the image key
            - annotator_id and reviewer_id may be null if not assigned
            - annotator_role and reviewer_role will be null if the respective user is not a project member
        """
        return self.client.get(f"projects/{project_id}/allocations/")

    def bulk_allocate_images(
        self,
        project_id: str,
        allocations: List[Dict[str, Any]],
        override_existing_work: bool = False,
    ) -> Dict[str, Any]:
        """
        Bulk allocate images to specific annotators and reviewers

        Args:
            project_id (str): The project ID
            allocations (list): List of allocation objects with the following structure:
                {
                    "image_key": "image1.jpg",
                    "annotators": ["annotator1@example.com", "annotator2@example.com"],
                    "reviewers": ["reviewer1@example.com", "reviewer2@example.com"]
                }
            override_existing_work (bool, optional): Whether to override existing work.
                Defaults to False.

        Returns:
            dict: Result of the allocation operation
        """
        data = {
            "allocations": allocations,
            "override_existing_work": override_existing_work,
        }
        return self.client.post(f"projects/{project_id}/bulk-allocate/", json=data)
