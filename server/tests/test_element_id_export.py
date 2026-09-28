from __future__ import annotations

import json
import unittest

from revit_model_mcp.revit_channel import JobPickupStatus, ReadJob, RevitReadChannel

EXPORT_RESPONSE = json.dumps(
    {
        "command": "export-element-ids",
        "success": True,
        "data": {
            "path": (
                "C:\\Users\\Administrator\\Documents\\RevitModelMcp\\Exports"
                "\\构件ID清单_MEP文件_20260928_153000.xlsx"
            ),
            "fileName": "构件ID清单_MEP文件_20260928_153000.xlsx",
            "sheetName": "构件ID清单",
            "columns": ["类别", "族", "类型", "标高", "构件ID", "名称", "工作集"],
            "rowCount": 1103,
            "totalCandidates": 1103,
            "truncated": False,
            "sizeBytes": 42112,
            "categoryCounts": [{"category": "管道", "count": 417}],
        },
        "elapsedMs": 1200,
    },
    ensure_ascii=False,
)


class ElementIdExportTests(unittest.IsolatedAsyncioTestCase):
    def test_forms_default_export_job(self) -> None:
        job = ReadJob.export_element_ids()

        self.assertEqual(job.payload, {"command": "export-element-ids"})
        # The workbook is written on the workstation, so the client keeps no download path.
        self.assertIsNone(job.save_to)

    def test_forms_export_job_with_fields_and_path(self) -> None:
        job = ReadJob.export_element_ids(["category", "id"], "C:\\Exports\\ids.xlsx")

        self.assertEqual(
            job.payload,
            {
                "command": "export-element-ids",
                "fields": ["category", "id"],
                "saveTo": "C:\\Exports\\ids.xlsx",
            },
        )
        self.assertIsNone(job.save_to)

    def test_ignores_blank_fields_and_path(self) -> None:
        job = ReadJob.export_element_ids(["", "   "], "   ")

        self.assertEqual(job.payload, {"command": "export-element-ids"})

    async def test_channel_surfaces_the_workbook_path_without_downloading(self) -> None:
        downloads: list[bool] = []

        class Remote:
            async def prepare_job(self, name, content, command):
                return set()

            async def wait_until_trigger_is_gone(self, timeout_seconds):
                return JobPickupStatus(True, 0, False, 0.1)

            async def wait_for_new_response(
                self, command, known_names, timeout_seconds, correlation_id=None
            ):
                return "response_export-element-ids.json"

            async def finish_job(self, response_name, cleanup_names, download_artifact, save_to):
                downloads.append(download_artifact)
                return EXPORT_RESPONSE, None

            async def delete_files(self, names):
                return None

        response = await RevitReadChannel(Remote()).execute(ReadJob.export_element_ids())

        self.assertEqual(response["data"]["rowCount"], 1103)
        self.assertEqual(response["data"]["sheetName"], "构件ID清单")
        self.assertTrue(response["data"]["path"].endswith(".xlsx"))
        self.assertEqual(response["data"]["categoryCounts"][0]["category"], "管道")
        # One finish call and no artifact download: the workbook stays on the workstation.
        self.assertEqual(downloads, [False])
