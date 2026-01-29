echo "BUILD START"

# Add --break-system-packages to bypass the PEP 668 error
python3 -m pip install -r requirements.txt --break-system-packages

python3 manage.py collectstatic --noinput --clear
echo "BUILD END"
