select 
        json_build_object(
            'ship_id',ship_id,
            'bearing',bearing,
            'location',json_build_object(
                'coords',json_build_object(
                    'lon', st_x(st_asText(location)),
                    'lat', st_y(st_asText(location))
                )
            ),
            'speed', speed,
            'hitpoints', 500
        )
        from ships;