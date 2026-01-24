import httpx
from ..config import JUDGE_API_URL, JUDGE_API_TIMEOUT_SECONDS
import logging

logger = logging.getLogger(__name__)

class JudgeService:
    def __init__(self):
        self.api_url = JUDGE_API_URL
        self.timeout = JUDGE_API_TIMEOUT_SECONDS

    async def judge_submission(self, question_id: str, code_answer: str) -> int:
        """
        Send code to external judge API for evaluation.
        
        Args:
            question_id: Question identifier (e.g., "E01", "M04", "H10")
            code_answer: The brocode-lang code submitted by the user
        
        Returns:
            int: 1 if correct, 0 if wrong
        
        Raises:
            Exception: If API call fails or returns invalid response
        """
        if not self.api_url:
            raise Exception("JUDGE_API_URL is not configured")

        payload = {
            "question_id": question_id,
            "code_answer": code_answer
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                response.raise_for_status()
                
                result_data = response.json()
                
                # Validate response format
                if "result" not in result_data:
                    logger.error(f"Invalid judge API response: {result_data}")
                    raise Exception("Invalid response from judge API: missing 'result' field")
                
                result = result_data["result"]
                
                # Ensure result is 0 or 1
                if result not in [0, 1]:
                    logger.error(f"Invalid result value from judge API: {result}")
                    raise Exception(f"Invalid result value: {result}. Expected 0 or 1")
                
                logger.info(f"Judge result for {question_id}: {result}")
                return result
                
        except httpx.TimeoutException:
            logger.error(f"Judge API timeout for question {question_id}")
            raise Exception("Judge API request timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"Judge API HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Judge API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Judge API call failed: {str(e)}")
            raise

# Singleton instance
judge_service = JudgeService()
