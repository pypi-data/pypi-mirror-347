import requests

class JThetaClient:
    def __init__(self, api_key: str, base_url: str = "https://api.jtheta.ai/api"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def validate_key(self):
        url = f"{self.base_url}/validate_key/"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_project(self, project_title: str, project_category: str):
        url = f"{self.base_url}/create_project/"
        payload = {
            "project_title": project_title,
            "project_category": project_category
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()







# import requests

# class Client:
#     def __init__(self, api_key: str, api_url: str = "http://127.0.0.1:8001/api"):
#         self.api_key = api_key
#         self.api_url = api_url.rstrip("/")
#         self.headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }

#     def validate_key(self):
#         url = f"{self.api_url}/validate_key/"
#         response = requests.get(url, headers=self.headers)
#         if response.status_code != 200:
#             print("Response Text:", response.text)  # ADD THIS
#         # response.raise_for_status()
#         return response.json()


#     def create_project(self, project_title: str, project_type: str, tier_name: str, workspace_name: str):
#         url = f"{self.api_url}/project/create/"
#         payload = {
#             "project_title": project_title,
#             "project_type": project_type,
#             "tier_name": tier_name,
#             "workspace_name": workspace_name
#         }
#         response = requests.post(url, headers=self.headers, json=payload)
#         return self._handle_response(response)


#     def create_dataset(self, dataset_name: str, license: str = "CC0-1.0", public: bool = True):
#         url = f"{self.api_url}/dataset/create/"
#         payload = {
#             "name": dataset_name,
#             "license": license,
#             "public": public
#         }
#         response = requests.post(url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()

#     def upload_images(self, dataset_id: str, image_paths: list):
#         # Will implement with progress bar
#         pass

#     def request_annotations(self, dataset_id: str, labels: dict, use_ai_assist: bool = True):
#         url = f"{self.api_url}/annotation/request/"
#         payload = {
#             "dataset_id": dataset_id,
#             "use_ai_assist": use_ai_assist,
#             "labels": labels
#         }
#         response = requests.post(url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()

#     def create_annotation(self, project_name: str, assigned_annotator: str, assigned_reviewer: str, labels: dict, allow_class_creation: bool = False, auto_annotation: bool = False):
#         url = f"{self.api_url}/annotation/create/"
#         payload = {
#             "project_name": project_name,
#             "assigned_annotator": assigned_annotator,
#             "assigned_reviewer": assigned_reviewer,
#             "labels": labels,
#             "allow_class_creation": allow_class_creation,
#             "auto_annotation": auto_annotation
#         }
#         response = requests.post(url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()

#     def check_annotation_status(self, project_title: str):
#         url = f"{self.api_url}/annotation/status/"
#         payload = {
#             "project_title": project_title
#         }
#         response = requests.post(url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()

#     def download_dataset(self, dataset_id: str, version: str, format: str):
#         url = f"{self.api_url}/dataset/download/"
#         payload = {
#             "dataset_id": dataset_id,
#             "version": version,
#             "format": format
#         }
#         response = requests.post(url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         download_link = response.json().get("url")
#         return download_link







# # import requests

# # class Client:
# #     def __init__(self, api_key: str, api_url: str = "http://127.0.0.1:8001/api"):
# #         self.api_key = api_key
# #         self.api_url = api_url.rstrip("/")
# #         self.headers = {
# #             "Authorization": f"Bearer {self.api_key}",
# #             "Content-Type": "application/json"
# #         }

# #     def validate_key(self):
# #         url = f"{self.api_url}/validate_key/"
# #         try:
# #             response = requests.get(url, headers=self.headers)
# #             response.raise_for_status()
# #             return {
# #                 "success": True,
# #                 "message": "API Key is valid.",
# #                 "data": response.json()
# #             }
# #         except requests.exceptions.HTTPError as err:
# #             return {
# #                 "success": False,
# #                 "message": f"Invalid API Key or server error: {err}",
# #                 "status_code": response.status_code,
# #                 "error": response.text
# #             }
