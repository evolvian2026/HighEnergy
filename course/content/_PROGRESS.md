# Doc import progress (for the portal "Learn" section)
Method: mcp__Claude_Docs__export (format markdown) -> copy bytes_b64 into `base64 -d > <M>-<role>.md`, check `wc -c` == bytes.
Docs (project id / tab file id):
M0 teacher d7ef157c-a0db-4a98-860b-01f9dad2a221 / fe431185-1f4f  DONE
M0 student 63f9f4fb-5ba4-4b1a-ab72-fcab0630bc4d / 5400e1ed-1cfb  DONE
M1 teacher 2d0e36b5-74e2-4ddb-a3dd-5c67e430dedb / 6e05d244-1e79  DONE
M1 student 7638beb9-9ec7-437b-8691-d5f5a4e4d5bf / e0f06216-aaa4  DONE
M2 teacher 49d74595-68c0-4183-9547-38834a37a070 / 0a5a5c78-7469  DONE
M2 student b3c22f65-d24f-4917-a5ff-cb2fc10c52d4 / d87b9fbf-ef67  DONE
M3 teacher d96f4222-ad00-426e-ba46-eec33bd9c6da / 91b6f7b4-ce5f  DONE
M3 student d4dfc03e-2df0-4791-a0ce-d3406f771b08 / b3effc61-1f25  DONE
M4 teacher 22f6f014-4a35-41d1-9cbb-c69125dba940 / a0bd966f-3a9a  DONE
M4 student 07a0eb75-63f5-48c5-b399-844c4ba2c47b / 41ae7551-a8d9  DONE
M5 teacher f9675e8c-0c34-48a6-abe3-d42b8bfad7e5 / 441d3ef6-454d  DONE
M5 student bda8bee2-1c8d-446e-bea7-2c3de2cba0ec / 2f5dc3fa-84b9  DONE
M6 teacher e2d4e6a2-57f2-462f-a6a1-eed85550f273 / 274603af-251d  DONE
M6 student 3282ca21-5e6e-4ee7-bba7-cc26aa8f20a9 / a472a15c-7275  DONE
M7 teacher ce565611-668f-4403-9d9e-e7a404ad4f71 / 7f91bfe7-c4e8  DONE
M7 student 0c46b157-6e58-4f36-845f-c9af7adaed99 / 18eae3bc-c3be  DONE
M8 teacher 2c717971-a5b8-48e5-aefc-2df9ed22f60e / 262cc444-54e1  DONE
M8 student fa7df325-0c5d-419a-95e7-a52bb7074546 / d9fa460a-ef59  DONE
M9 teacher db012558-e896-49e6-9fee-13a9c067024d / 96761f46-2a1b  DONE
M9 student 19dae601-4d06-49b2-b51c-cc5ff36c0e2c / e4b8327f-253d  DONE
M10 teacher 2a71e86b-cd00-44c1-ab12-d1c01d724f84 / e86f1125-bfc8  DONE
M10 student 453f3646-b3f4-467c-a517-153b3eba5d49 / 623f0717-7bf7  DONE
M11 teacher ea2f2585-96d5-41b7-949b-40b003e5154e / a6331889-e60d  DONE
M11 student c1269b00-13fa-4bfe-9b65-5e1c2628e2e9 / 137d67b3-a868  DONE

Portal plan: Learn view (module picker, lecture tabs, accordion sections, C++/Java code toggle,
self-check quizzes, mark-section-read progress). Student content bundled in both builds.
Teacher guides: artifact build only, stored in db at teacher/{M} (admin-only read) -> staff see
"Teacher guide" tab; public site never ships them. Staff can "release answers" per lecture.
