# Notifier App

```
pip-compile
pip-sync
pre-commit install
./manage createsuperuser
./manage.py addfriends USERNAME
```

## Todo

- Modularize settings (base, dev, prod)

## Notes

```
# local vs utc datetime
dt_la = datetime.datetime.now(tz=pytz.timezone('America/Los_Angeles'))
dt_utc = dt_la.astimezone(pytz.utc)
```
