"""Module for writting data to the database."""


def insert_tb_energy_data() -> str:
    """Insert the tb_energy_data table into the database.

    Returns:
        str: The query to insert the data.
    """
    return """INSERT INTO solaxcloud.tb_energy_data (
                fecha, periodo, min, inverter_id, acpower, yieldtoday, yieldtotal,
                feedinpower, feedinenergy, consumeenergy, uploadTime
            ) VALUES (
                %(fecha)s, %(periodo)s, %(min)s, %(inverter_id)s, %(acpower)s, %(yieldtoday)s,
                %(yieldtotal)s, %(feedinpower)s, %(feedinenergy)s, %(consumeenergy)s, %(uploadTime)s
            ) ON DUPLICATE KEY UPDATE
                acpower = VALUES(acpower),
                yieldtoday = VALUES(yieldtoday),
                yieldtotal = VALUES(yieldtotal),
                feedinpower = VALUES(feedinpower),
                feedinenergy = VALUES(feedinenergy),
                consumeenergy = VALUES(consumeenergy),
                uploadTime = VALUES(uploadTime);"""


def insert_tb_battery_data() -> str:
    """Insert the tb_battery_data table into the database.

    Returns:
        str: The query to insert the data.
    """
    return """INSERT INTO solaxcloud.tb_battery_data (
                fecha, periodo, min, inverter_id, batPower, soc, batStatus, uploadTime
            ) VALUES (
                %(fecha)s, %(periodo)s, %(min)s, %(inverter_id)s, %(batPower)s, %(soc)s,
                %(batStatus)s, %(uploadTime)s
            ) ON DUPLICATE KEY UPDATE
                batPower = VALUES(batPower),
                soc = VALUES(soc),
                batStatus = VALUES(batStatus),
                uploadTime = VALUES(uploadTime);"""


def insert_tb_phase_power_data() -> str:
    """Insert the tb_phase_power_data table into the database.

    Returns:
        str: The query to insert the data.
    """
    return """INSERT INTO solaxcloud.tb_phase_power_data (
            fecha, periodo, min, inverter_id, peps1, peps2, peps3, powerdc1, powerdc2, powerdc3, powerdc4, uploadTime
        ) VALUES (
            %(fecha)s, %(periodo)s, %(min)s, %(inverter_id)s, %(peps1)s, %(peps2)s, %(peps3)s,
            %(powerdc1)s, %(powerdc2)s, %(powerdc3)s, %(powerdc4)s, %(uploadTime)s
        ) ON DUPLICATE KEY UPDATE
            peps1 = VALUES(peps1),
            peps2 = VALUES(peps2),
            peps3 = VALUES(peps3),
            powerdc1 = VALUES(powerdc1),
            powerdc2 = VALUES(powerdc2),
            powerdc3 = VALUES(powerdc3),
            powerdc4 = VALUES(powerdc4),
            uploadTime = VALUES(uploadTime);"""


def insert_weatherbit_current() -> str:
    """
    Devuelve la consulta SQL para insertar datos.
    """
    return """
        INSERT INTO weatherbit.tb_hourly_data (
            calculation_datetime, app_temp, aqi, city_name, clouds, country_code, datetime,
            dewpt, dhi, dni, elev_angle, ghi, gust, h_angle, lat, lon, ob_time, pod, precip,
            pres, rh, slp, snow, solar_rad, sources, state_code, station, sunrise, sunset, temp,
            timezone, ts, uv, vis, weather_icon, weather_description, weather_code,
            wind_cdir, wind_cdir_full, wind_dir, wind_spd
        )
        VALUES (
            %(calculation_datetime)s, %(app_temp)s, %(aqi)s, %(city_name)s, %(clouds)s, %(country_code)s,
            %(datetime)s, %(dewpt)s, %(dhi)s, %(dni)s, %(elev_angle)s, %(ghi)s, %(gust)s,
            %(h_angle)s, %(lat)s, %(lon)s, %(ob_time)s, %(pod)s, %(precip)s, %(pres)s, %(rh)s,
            %(slp)s, %(snow)s, %(solar_rad)s, %(sources)s, %(state_code)s, %(station)s, %(sunrise)s,
            %(sunset)s, %(temp)s, %(timezone)s, %(ts)s, %(uv)s, %(vis)s, %(weather_icon)s,
            %(weather_description)s, %(weather_code)s, %(wind_cdir)s, %(wind_cdir_full)s, %(wind_dir)s,
            %(wind_spd)s
        )
        ON DUPLICATE KEY UPDATE
            app_temp = VALUES(app_temp),
            aqi = VALUES(aqi),
            clouds = VALUES(clouds),
            country_code = VALUES(country_code),
            datetime = VALUES(datetime),
            dewpt = VALUES(dewpt),
            dhi = VALUES(dhi),
            dni = VALUES(dni),
            elev_angle = VALUES(elev_angle),
            ghi = VALUES(ghi),
            gust = VALUES(gust),
            h_angle = VALUES(h_angle),
            lat = VALUES(lat),
            lon = VALUES(lon),
            ob_time = VALUES(ob_time),
            pod = VALUES(pod),
            precip = VALUES(precip),
            pres = VALUES(pres),
            rh = VALUES(rh),
            slp = VALUES(slp),
            snow = VALUES(snow),
            solar_rad = VALUES(solar_rad),
            sources = VALUES(sources),
            state_code = VALUES(state_code),
            station = VALUES(station),
            sunrise = VALUES(sunrise),
            sunset = VALUES(sunset),
            temp = VALUES(temp),
            timezone = VALUES(timezone),
            ts = VALUES(ts),
            uv = VALUES(uv),
            vis = VALUES(vis),
            weather_icon = VALUES(weather_icon),
            weather_description = VALUES(weather_description),
            weather_code = VALUES(weather_code),
            wind_cdir = VALUES(wind_cdir),
            wind_cdir_full = VALUES(wind_cdir_full),
            wind_dir = VALUES(wind_dir),
            wind_spd = VALUES(wind_spd);
    """


def insert_weatherbit_requests_log() -> str:
    """
    Devuelve la consulta SQL para insertar registros en tb_requests_log.
    """
    return """
        INSERT INTO weatherbit.tb_requests_log (request_datetime, status)
        VALUES (%(request_datetime)s, %(status)s)
        ON DUPLICATE KEY UPDATE status = VALUES(status);
    """


def insert_openweather_requests_log() -> str:
    """
    Devuelve la consulta SQL para insertar registros en tb_requests_log.
    """
    return """
        INSERT INTO openweather.tb_requests_log (request_datetime, request_option_id, status)
        VALUES (%(request_datetime)s, %(request_option_id)s, %(status)s)
        ON DUPLICATE KEY UPDATE status = VALUES(status);
        """


def insert_openweather_current() -> str:
    """
    Devuelve la consulta SQL para insertar registros en tb_current_weather.
    """
    return """
        INSERT INTO openweather.tb_current_weather (
    calculation_datetime, city_name, country, lat, lon, temp, feels_like, temp_min,
    temp_max, pressure, humidity, sea_level, grnd_level, visibility, wind_speed,
    wind_deg, wind_gust, clouds, dt, sunrise, sunset, weather_main, weather_description,
    weather_icon, timezone, base, city_id, sys_type, sys_id, rain_1h, rain_3h
)
VALUES (
    %(calculation_datetime)s, %(city_name)s, %(country)s, %(lat)s, %(lon)s, %(temp)s, %(feels_like)s, %(temp_min)s,
    %(temp_max)s, %(pressure)s, %(humidity)s, %(sea_level)s, %(grnd_level)s, %(visibility)s, %(wind_speed)s,
    %(wind_deg)s, %(wind_gust)s, %(clouds)s, %(dt)s, %(sunrise)s, %(sunset)s, %(weather_main)s, %(weather_description)s,
    %(weather_icon)s, %(timezone)s, %(base)s, %(city_id)s, %(sys_type)s, %(sys_id)s, %(rain_1h)s, %(rain_3h)s
)
ON DUPLICATE KEY UPDATE
    city_name = VALUES(city_name),
    country = VALUES(country),
    lat = VALUES(lat),
    lon = VALUES(lon),
    temp = VALUES(temp),
    feels_like = VALUES(feels_like),
    temp_min = VALUES(temp_min),
    temp_max = VALUES(temp_max),
    pressure = VALUES(pressure),
    humidity = VALUES(humidity),
    sea_level = VALUES(sea_level),
    grnd_level = VALUES(grnd_level),
    visibility = VALUES(visibility),
    wind_speed = VALUES(wind_speed),
    wind_deg = VALUES(wind_deg),
    wind_gust = VALUES(wind_gust),
    clouds = VALUES(clouds),
    dt = VALUES(dt),
    sunrise = VALUES(sunrise),
    sunset = VALUES(sunset),
    weather_main = VALUES(weather_main),
    weather_description = VALUES(weather_description),
    weather_icon = VALUES(weather_icon),
    timezone = VALUES(timezone),
    base = VALUES(base),
    sys_type = VALUES(sys_type),
    sys_id = VALUES(sys_id),
    rain_1h = VALUES(rain_1h),
    rain_3h = VALUES(rain_3h);
    """


def insert_openweather_air_pollution() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return """
        INSERT INTO openweather.tb_air_pollution (
            calculation_datetime, lat, lon, dt, aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3
        )
        VALUES (
            %(calculation_datetime)s, %(lat)s, %(lon)s, %(dt)s, %(aqi)s, %(co)s, %(no)s, %(no2)s, %(o3)s, %(so2)s, %(pm2_5)s, %(pm10)s, %(nh3)s
        )
        ON DUPLICATE KEY UPDATE
            aqi = VALUES(aqi),
            co = VALUES(co),
            no = VALUES(no),
            no2 = VALUES(no2),
            o3 = VALUES(o3),
            so2 = VALUES(so2),
            pm2_5 = VALUES(pm2_5),
            pm10 = VALUES(pm10),
            nh3 = VALUES(nh3);
    """


def insert_tb_notification_log() -> str:
    """
    Inserta o actualiza el timestamp de una notificación por inversor y tipo.
    """
    return """
        INSERT INTO solaxcloud.tb_notification_log (inverter_id, notification_type, sent_at)
        VALUES (%(inverter_id)s, %(notification_type)s, %(sent_at)s)
        ON DUPLICATE KEY UPDATE sent_at = VALUES(sent_at);
    """
