#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
TODO: add type as a required parameter (photo etc)
*) upload the whole csv into one table, separate, add ids
*) whole_tsv_dump should be temporary, clear after each upload
"""
import sys
import util

try:
  import mysqlclient as mysql
except ImportError:
  try:
    import pymysql as mysql
  except ImportError:
    import MySQLdb as mysql

import argparse
from collections import defaultdict


class Metadata:
  # parse csv

  metadata_to_field = {
    "Metadata.Type"              : "metadata_type",
    "Identifier"                 : "identifier",
    "Title"                      : "title",
    "Content"                    : "content",
    "Content URL"                : "content_url",
    "Creator"                    : "creator",
    "Creator.Other"              : "creator_other",
    "Subject.Place"              : "subject_place",
    "Coverage.Lat"               : "coverage_lat",
    "Coverage.Long"              : "coverage_long",
    "Subject.Associated.Places"  : "subject_associated_places",
    "Subject.People"             : "subject_people",
    "Subject.Academic.Field"     : "subject_academic_field",
    "Subject.Other"              : "subject_other",
    "Subject.Season"             : "subject_season",
    "Date.Season"                : "date_season",
    "Date.Season (YYYY)"         : "date_season_yyyy",
    "Date.Exact"                 : "date_exact",
    "Date.Digital"               : "date_digital",
    "Description"                : "description",
    "Format"                     : "format",
    "Digitization Specifications": "digitization_specifications",
    "Contributor"                : "contributor",
    "Type"                       : "type",
    "Country"                    : "country",
    "Language"                   : "language",
    "Relation"                   : "relation",
    "Source"                     : "source",
    "Publisher"                  : "publisher",
    "Publisher Location"         : "publisher_location",
    "Bibliographic Citation"     : "bibliographic_citation",
    "Rights"                     : "rights"
  }

  def __init__(self, input_file):
    self.tsv_file_content_list = []
    self.tsv_file_content_dict = {}
    self.get_data_from_csv(input_file)
    self.tsv_file_fields = self.tsv_file_content_list[0]
    self.transposed_vals = list(map(list, zip(*self.tsv_file_content_list[1])))

    self.not_empty_tsv_content_dict = self.check_for_empty_fields()

    self.not_empty_tsv_content_dict = self.change_keys_in_tsv_content_dict_clean_custom(
      self.not_empty_tsv_content_dict)
    self.tsv_file_fields = list(self.not_empty_tsv_content_dict.keys())

    self.tsv_file_content_dict_no_empty = self.format_not_empty_dict()
    self.check_for_empty_keys()

    self.tsv_file_content_dict_clean_keys = self.clean_keys_in_tsv_file_content_dict()

  def clean_keys_in_tsv_file_content_dict(self):
    res_d = []
    for curr_d in self.tsv_file_content_dict:
      clean_d = self.change_keys_in_tsv_content_dict_clean_custom(curr_d)
      res_d.append(clean_d)
    return res_d

  def check_for_empty_keys(self):
    all_fields = self.tsv_file_content_list[0]
    if "" in all_fields:
      print("ERROR: Column (field names) shouldn't be empty!")
      sys.exit()

  def get_data_from_csv(self, input_file):
    self.tsv_file_content_list = utils.read_csv_into_list(input_file, "\t")
    self.tsv_file_content_dict = utils.read_csv_into_dict(input_file, "\t")

  def format_not_empty_dict(self):
    temp_list_of_dict = []
    keys = list(self.not_empty_tsv_content_dict.keys())
    transposed_values = list(map(list, zip(*self.not_empty_tsv_content_dict.values())))
    for line in transposed_values:
      temp_dict = {}
      for idx, v in enumerate(line):
        key = keys[idx]
        temp_dict[key] = v
      temp_list_of_dict.append(temp_dict)
    return temp_list_of_dict

  def check_for_empty_fields(self):
    removed_fields = []
    clean_matrix = []
    good_fields = []
    for idx, vals_l in enumerate(self.transposed_vals):
      all_val_for1_field = set(vals_l)
      field_name = self.tsv_file_fields[idx]
      if any(all_val_for1_field):
        good_fields.append(field_name)
        clean_matrix.append(vals_l)
      else:
        removed_fields.append(field_name)
    not_empty_tsv_content_dict = dict(zip(good_fields, clean_matrix)) or {}

    return not_empty_tsv_content_dict

  def change_keys_in_tsv_content_dict_clean_custom(self, my_dict):
    return {field_name.replace(".", "_").replace(" ", "_").replace("(", "").replace(")", "").lower(): val
            for field_name, val in my_dict.items()}


class Upload:
  """
  table types (intersect is possible):
  *) table_name equal field_name ("identifier")
  *) many field_names correspond to one table_name = field_name ("place": ["subject_associated_places", "subject_place"]}), see many_values_to_one_field
  *) tables with foreign keys, see table_names_w_ids
  """

  table_names_w_ids = ["entry"]
  table_names_to_ignore = ["entry_view"]
  table_name_temp_dump = "whole_tsv_dump"
  many_values_to_one_field = {
    "season": ["date_digital", "date_exact", "date_season", "date_season_yyyy", "subject_season"],
    "person": ["contributor", "creator", "creator_other", "subject_people"],
    "place":  ["country", "publisher_location", "subject_associated_places", "subject_place"]
  }

  where_to_look_if_not_the_same = {
    # "bibliographic_citation"   : "source.bibliographic_citation",
    # "content": "content",
    # "content_url"              : "content.content_url",
    "contributor"                 : "person",
    "country"                     : "place",
    # "coverage_lat": "coverage_lat",
    # "coverage_long": "coverage_long",
    "creator"                     : "person",
    "creator_other"               : "person",
    "date_digital"                : "season",
    "date_exact"                  : "season",
    "date_season"                 : "season",
    "date_season_yyyy"            : "season",
    # "description"              : "content.description",
    # "digitization_specifications": "digitization_specifications",
    # "format": "format",
    # "identifier": "identifier",
    # "language": "language",
    # "publisher"                : "publisher",
    "publisher_location"          : "place",
    # "relation": "relation",
    # "rights"                   : "source.rights",
    # "source": "source",
    "subject_academic_field"      : "subject_academic_field",
    "subject_associated_places"   : "place",
    # "subject_other": "subject_other",
    "subject_people"              : "person",
    "subject_place"               : "place",
    "subject_season"              : "season",
    # "title"                    : "content.title",
    # "type": "type",
  }

  foreign_key_tables = defaultdict(dict)

  def __init__(self):
    """
        1) upload simple tables (table_names_simple)
        2) upload combine tables no foreign keys (content, person, place, season, source)
        3) get ids
        4) upload tables with ids
    """

    self.many_values_to_one_field_column_names = utils.flatten_2d_list(self.many_values_to_one_field.values())
    self.special_tables = self.get_special_tables()
    self.simple_tables = list(all_tables_set - set(self.special_tables))

    self.drop_temp_table()
    self.create_temp_table()

    self.upload_empty()
    self.upload_simple_tables()
    self.upload_all_from_tsv_into_temp_table()
    self.mass_update_simple_ids()

    self.upload_many_values_to_one_field()
    self.update_many_values_to_one_field_ids()

    self.upload_other_tables()

    print("here")

  def drop_temp_table(self):
    drop_query = "DROP TABLE IF EXISTS {}".format(self.table_name_temp_dump)
    mysql_utils.execute_no_fetch(drop_query)

  def create_temp_table(self):
    create_table_q = """
    CREATE TABLE IF NOT EXISTS `{0}` (
      `{0}_id` int(11) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
      `created` datetime DEFAULT current_timestamp(),
      `updated` datetime DEFAULT NULL
    ) ENGINE=InnoDB;
    """.format(self.table_name_temp_dump)
    mysql_utils.execute_no_fetch(create_table_q)

    all_fields = metadata.metadata_to_field.values()
    column_names_w_ids = [x + "_id" for x in all_fields]
    #           ADD COLUMN `ping_status` INT(1) NOT NULL AFTER
    #   `bibliographic_citation` varchar(512) DEFAULT '',
    #   `bibliographic_citation_id` int(11) unsigned NOT NULL,
    column_names_arr = []
    column_names_str_begin = "ALTER TABLE {}".format(self.table_name_temp_dump)
    for c_name_w_id in column_names_w_ids:
      add_col_str_w_id = " ADD COLUMN {} int(11) UNSIGNED NOT NULL".format(c_name_w_id)
      column_names_arr.append(add_col_str_w_id)
    for c_name in all_fields:
      add_col_str = ' ADD COLUMN {} varchar(1024) DEFAULT ""'.format(c_name)
      column_names_arr.append(add_col_str)

    column_names_str_end = " ADD UNIQUE KEY title (title)"
    column_names_arr.append(column_names_str_end)

    column_names_str = ", ".join(column_names_arr)
    add_columns_q = column_names_str_begin + column_names_str
    mysql_utils.execute_no_fetch(add_columns_q)

    # print("QQ")

  def get_special_tables(self):
    special_tables = [self.table_name_temp_dump]
    return special_tables + self.table_names_to_ignore + self.table_names_w_ids + list(self.many_values_to_one_field.keys())
    # ["entry", "person", "place", "season", "whole_tsv_dump"]

  def upload_empty(self):
    all_tables_set.discard(self.table_names_w_ids[0])
    all_tables_set.discard(self.table_names_to_ignore[0])
    for table_name in list(all_tables_set):
      insert_query = "INSERT IGNORE INTO `{}` (`{}`) VALUES (NULL)".format(table_name, table_name + "_id")
      mysql_utils.execute_no_fetch(insert_query)

  def upload_simple_tables(self):
    for table_name in self.simple_tables:
      self.simple_mass_upload(table_name, table_name)

  def simple_mass_upload(self, table_name, field_name, val_arr = []):
    try:
      if not val_arr:
        val_arr = list(set(metadata.not_empty_tsv_content_dict[field_name]))
      mysql_utils.execute_insert_many(table_name, field_name, val_arr)

    except KeyError:
      insert_query = "INSERT IGNORE INTO `{}` (`{}`) VALUES (NULL)".format(table_name, table_name + "_id")
      mysql_utils.execute_no_fetch(insert_query)

  def make_field_val_couple_where(self, field_names_arr, values_arr):
    # TODO: confirm that a "title" is unique and use just it to get an id
    couples_arr = ['{} = "{}"'.format(t[0], t[1]) for t in zip(field_names_arr, values_arr)]
    return 'WHERE ' + ' AND '.join(couples_arr)

  # def insert_row(self, table_name, field_names_arr, values_tuple):
  #   field_names_str = ', '.join(field_names_arr)
  #   values_str_pattern = ", ".join(['%s' for e in field_names_arr])

    # mySql_insert_query = "INSERT {} INTO {} ({}) VALUES ({})".format("IGNORE", table_name, field_names_str, values_str_pattern)

    # mysql_utils.execute_insert_many(table_name, field_names_str, values_str_pattern)
    # mysql_utils.cursor.execute(mySql_insert_query, values_tuple)

  def upload_all_from_tsv_into_temp_table(self):
    table_name = self.table_name_temp_dump
    table_name_id = table_name + "_id"
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      field_names_arr = list(current_row_d.keys())

      mysql_utils.execute_many_fields_one_record(table_name, field_names_arr, tuple(current_row_d.values()))

      # separate as add_id_back
      values_arr = list(current_row_d.values())
      where_part_for_id = self.make_field_val_couple_where(field_names_arr, values_arr)
      current_id = mysql_utils.get_id(table_name_id, table_name, where_part_for_id)
      current_row_d[table_name_id] = current_id

  def mass_update_simple_ids(self):
    for table_name in self.simple_tables:
      try:
        current_vals = set(metadata.not_empty_tsv_content_dict[table_name])
      except KeyError:
        # is empty
        continue

      field_name = table_name
      field_name_id = field_name + '_id'
      current_vals_str = ', '.join('"{0}"'.format(w) for w in current_vals)

      select_q = """SELECT {}, {} FROM {} WHERE {} in ({});
      """.format(field_name, field_name_id, table_name, field_name, current_vals_str)
      sql_res = mysql_utils.execute_fetch_select(select_q)

      for (val, val_id) in sql_res[0]:
        update_q = '''UPDATE {}
          SET {} = {} 
          WHERE {} = "{}"'''.format(self.table_name_temp_dump, field_name_id, val_id, field_name, val)
        mysql_utils.execute_no_fetch(update_q)

  def upload_many_values_to_one_field(self):
    tsv_field_names_to_upload = self.many_values_to_one_field_column_names
    value_present = utils.intersection(tsv_field_names_to_upload, metadata.not_empty_tsv_content_dict.keys())

    for table_name, tsv_field_names in self.many_values_to_one_field.items():
      for tsv_field_name in tsv_field_names:
        if tsv_field_name in value_present:
          val_arr = list(set(metadata.not_empty_tsv_content_dict[tsv_field_name]))
          self.simple_mass_upload(table_name, table_name, val_arr)

  def update_many_values_to_one_field_ids(self):
    table_name_to_update = self.table_name_temp_dump
    tsv_field_names_to_upload = utils.flatten_2d_list(self.many_values_to_one_field.values())
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      """TODO: go over each table values instead?     
      for table_name, tsv_field_names in self.many_values_to_one_field.items():"""
      for tsv_field_name in tsv_field_names_to_upload:
        try:
          current_value = current_row_d[tsv_field_name]
        except KeyError:
          continue
        table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
        where_part = 'WHERE {} = "{}"'.format(table_name_w_id, current_value)
        current_id = mysql_utils.get_id(table_name_w_id + '_id', table_name_w_id, where_part)
        # TODO: update these in columns rather then in rows (all data_exact where == 1976 etc.)
        update_q = 'UPDATE {} SET {} = {} WHERE {} = "{}"'.format(table_name_to_update, tsv_field_name + '_id', current_id, tsv_field_name, current_value)
        mysql_utils.execute_no_fetch(update_q)

  def find_empty_ids(self, sql_res_d):
    for field, val in sql_res_d.items():
      if val == 0:
        name_no_id = field[:-3]
        '''select identifier_id from identifier where identifier = ""'''
        select_q = 'SELECT {} FROM {} WHERE {} = ""'.format(field, name_no_id, name_no_id)
        empty_id = mysql_utils.execute_fetch_select(select_q)
        sql_res_d[field] = list(utils.extract(empty_id))[0]
    return sql_res_d

  def upload_other_tables(self):
    table_name_to_update = self.table_names_w_ids[0] # ["entry"]
    where_to_look_for_ids = self.table_name_temp_dump
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      tsv_field_names_to_upload = current_row_d.keys()
      tsv_field_names_to_upload_ids = [x+"_id" for x in tsv_field_names_to_upload if not x.endswith("_id")]
      tsv_field_names_to_upload_ids_str = ', '.join(tsv_field_names_to_upload_ids)
      unique_key = 'title'
      select_q = '''SELECT {} FROM {} 
        WHERE {} = "{}"'''.format(tsv_field_names_to_upload_ids_str, where_to_look_for_ids, unique_key, current_row_d['title'])
      sql_res = mysql_utils.execute_fetch_select_to_dict(select_q)
      dict_w_all_ids = self.find_empty_ids(sql_res[0])
      # IF empty and no id - get
      #     def execute_many_fields_one_record(self, table_name, field_names_arr, values_tuple, ignore = "IGNORE"):
      mysql_utils.execute_many_fields_one_record(table_name_to_update, list(dict_w_all_ids.keys()), tuple(dict_w_all_ids.values()))


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.csv

  utils = util.Utils()


  if utils.is_local():
    db_schema = 'mcm_history'
    mysql_utils = util.Mysql_util(host = 'localhost', db = db_schema, read_default_group = 'clienthome')
    print("host = 'localhost', db = {}".format(db_schema))
  else:
    db_schema = 'mcmurdohistory_metadata'
    mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = db_schema, read_default_group = 'client')
    print("host = 'taylor.unm.edu', db {}".format(db_schema))

  all_tables_sql_res = mysql_utils.get_table_names(db_schema)
  all_tables_set = set(utils.extract(all_tables_sql_res[0]))

  parser = argparse.ArgumentParser()

  parser.add_argument('-f', '--file_name',
                      required = True, action = 'store', dest = 'input_file',
                      help = '''Input file name''')
  parser.add_argument("-ve", "--verbatim",
                      required = False, action = "store_true", dest = "is_verbatim",
                      help = """Print an additional inforamtion""")

  args = parser.parse_args()
  print('args = ')
  print(args)

  is_verbatim = args.is_verbatim

  metadata = Metadata(args.input_file)
  upload_metadata = Upload()