# test_import.py


def main():
    try:
        # พยายามนำเข้าโมดูล process_image
        from worker.tasks_module import process_image

        print("Successfully imported 'process_image' from 'app.worker.tasks_module'.")

        # เรียกใช้ฟังก์ชันเพื่อทดสอบ
        process_image("/app/app/static/uploads/test1.jpg")
        print("Function 'process_image' executed successfully.")

    except ImportError as ie:
        print(f"ImportError: {ie}")
    except AttributeError as ae:
        print(f"AttributeError: {ae}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
