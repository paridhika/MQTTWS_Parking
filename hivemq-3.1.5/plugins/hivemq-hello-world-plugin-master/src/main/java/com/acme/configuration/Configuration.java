/*
 * Copyright 2015 dc-square GmbH
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.acme.configuration;

import com.google.inject.Inject;

import java.util.Properties;

/**
 * @author Christian Götz
 */
public class Configuration {


    private final Properties properties;
    //Paridhika
    private static int SIZE = 100;
	private static String[][] my_map = new String[SIZE][SIZE];

    public String[][] getMap(){
    	return my_map;
    }
    
    public void initializeMap() {
		for (int i = 0; i < SIZE; i++) {
			for (int j = 0; j < SIZE; j++) {
				my_map[i][j] = "EMPTY";
			}
		}
	}

 // Paridhika
 	public static String findLocation() {
 		for (int i = 0; i < SIZE; i++) {
 			for (int j = 0; j < SIZE; j++) {
 				if (my_map[i][j].equals("EMPTY")) {
 					my_map[i][j] = "OCCUPIED";
 					return i + "," + j;
 				}
 			}
 		}
 		return null;
 	}
 	
 	public static void putLocation(String location) {
 		int x = Integer.parseInt(location.substring(0, location.indexOf(',')));
 		int y = Integer.parseInt(location.substring(location.indexOf(',') + 1));
 		if (my_map[x][y].equals("EMPTY")) {
 			my_map[x][y] = "OCCUPIED";
 		}
 	}

 	public static void deleteLocation(String location) {
 		int x = Integer.parseInt(location.substring(0, location.indexOf(',')));
 		int y = Integer.parseInt(location.substring(location.indexOf(',') + 1));
 		if (my_map[x][y].equals("OCCUPIED")) {
 			my_map[x][y] = "EMPTY";
 		}
 	}

 	public static void printMap() {
 		System.out.println();
 		for (int i = 0; i < SIZE; i++) {
 			for (int j = 0; j < SIZE; j++)
 				System.out.print(my_map[i][j] + " ");
 			System.out.println();
 		}
 	}

    
    @Inject
    public Configuration(PluginReader pluginReader) {
        properties = pluginReader.getProperties();
    }

    public String getMyProperty() {
        if (properties == null) {
            return null;
        }

        return properties.getProperty("myProperty");
    }
}
