def drop_global_data_from_revenue(revenue):
    revenue = revenue.copy()
    revenue = revenue.drop(columns=['Global']).dropna().reset_index(drop=True)
    return revenue

def impute_story_part(story_jp):
    story_jp = story_jp.copy()
    story_jp['Part'] = story_jp['Part'].astype(object)
    story_jp['Part'] = story_jp['Part'].fillna('None')
    return story_jp

def remove_rerun_prefix(event_jp):
    event_jp = event_jp.copy()
    event_jp['Name (EN)'] = event_jp['Name (EN)'].str.removeprefix('(Rerun) ')
    return event_jp

def mark_duplicates_as_rerun(event_jp):
    event_jp = event_jp.copy()

    original_or_rerun = event_jp['Name (EN)'].duplicated().map({True: 'Rerun', False: 'Original'})
    event_jp['Notes'] = event_jp['Notes'].fillna(original_or_rerun)
    return event_jp

def group_all_operation_events_together(event_jp):
    event_jp = event_jp.copy()
    event_jp.loc[event_jp["Notes"].str.contains("Operation", case=False, na=False), "Notes"] = "Operation"
    return event_jp

def clean_event_data(event_jp):
    event_jp = remove_rerun_prefix(event_jp)
    event_jp = mark_duplicates_as_rerun(event_jp)
    event_jp = group_all_operation_events_together(event_jp)
    return event_jp