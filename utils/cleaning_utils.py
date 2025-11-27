from __future__ import annotations

import pandas as pd

def drop_global_data_from_revenue(revenue: pd.DataFrame) -> pd.DataFrame:
    '''
    Drops global revenue from the revenue dataframe.

    Parameters
    ----------
    revenue : pd.DataFrame
        The revenue dataframe from which global revenue will be dropped.

    Returns
    -------
    pd.DataFrame
        The revenue dataframe with global revenue dropped.
    '''
    revenue = revenue.copy()
    revenue = revenue.drop(columns=['Global']).dropna().reset_index(drop=True)
    return revenue

def impute_story_part(story_jp: pd.DataFrame) -> pd.DataFrame:
    '''
    Imputes missing story parts with 'None'.

    Parameters
    ----------
    story_jp : pd.DataFrame
        Dataframe containing story information

    Returns
    -------
    pd.DataFrame
        Dataframe with missing story parts imputed as 'None'.
    '''
    story_jp = story_jp.copy()
    story_jp['Part'] = story_jp['Part'].astype(object)
    story_jp['Part'] = story_jp['Part'].fillna('None')
    return story_jp

def remove_rerun_prefix(event_jp: pd.DataFrame) -> pd.DataFrame:
    '''
    Removes the '(Rerun) ' prefix from event names.

    Parameters
    ----------
    event_jp : pd.DataFrame
        Dataframe containing event information.

    Returns
    -------
    pd.DataFrame
        Dataframe with '(Rerun) ' prefix removed from event names.
    '''
    event_jp = event_jp.copy()
    event_jp['Name (EN)'] = event_jp['Name (EN)'].str.removeprefix('(Rerun) ')
    return event_jp

def mark_duplicates_as_rerun(event_jp: pd.DataFrame) -> pd.DataFrame:
    '''
    Marks duplicate event names as 'Rerun' in the 'Notes' column.

    Parameters
    ----------
    event_jp : pd.DataFrame
        Dataframe containing event information.

    Returns
    -------
    pd.DataFrame
        Dataframe with duplicates marked as 'Rerun' in the 'Notes' column.
    '''
    event_jp = event_jp.copy()

    original_or_rerun = event_jp['Name (EN)'].duplicated().map({True: 'Rerun', False: 'Original'})
    event_jp['Notes'] = event_jp['Notes'].fillna(original_or_rerun)
    return event_jp

def group_all_operation_events_together(event_jp: pd.DataFrame) -> pd.DataFrame:
    '''
    Groups all operation events under the 'Operation' label in the 'Notes' column.

    Parameters
    ----------
    event_jp : pd.DataFrame
        Dataframe containing event information.

    Returns
    -------
    pd.DataFrame
        Dataframe with all operation events grouped under 'Operation' in the 'Notes' column.
    '''

    event_jp = event_jp.copy()
    event_jp.loc[event_jp["Notes"].str.contains("Operation", case=False, na=False), "Notes"] = "Operation"
    return event_jp

def clean_event_data(event_jp):
    '''
    Cleans the event data by removing rerun prefixes, marking duplicates as reruns,
    and grouping all operation events together. (combination of above functions)

    Parameters
    ----------
    event_jp : pd.DataFrame
        Dataframe containing event information.

    Returns
    -------
    pd.DataFrame
        Cleaned event dataframe.
    '''
    event_jp = remove_rerun_prefix(event_jp)
    event_jp = mark_duplicates_as_rerun(event_jp)
    event_jp = group_all_operation_events_together(event_jp)
    return event_jp