To run this project:
- deploy using `kubectl apply -f deployment/`
- wait till postgres datbase created. initialize database using `sh scripts/run_db_commands.sh postgress_pod_id`
- browse application

Note:
- The frontend build is static, current version using minikube and fixed at my local minikube ip. Therefore if use different host, need to update variable `REACT_APP_API_HOST` in `.env` or `.env.development`