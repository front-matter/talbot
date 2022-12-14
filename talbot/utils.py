import os
import json
import html
import re
from .doi_utils import normalize_doi
from urllib.parse import urlparse

NORMALIZED_LICENSES = {
    'https://creativecommons.org/licenses/by/1.0': 'https://creativecommons.org/licenses/by/1.0/legalcode',
    'https://creativecommons.org/licenses/by/2.0': 'https://creativecommons.org/licenses/by/2.0/legalcode',
    'https://creativecommons.org/licenses/by/2.5': 'https://creativecommons.org/licenses/by/2.5/legalcode',
    'https://creativecommons.org/licenses/by/3.0': 'https://creativecommons.org/licenses/by/3.0/legalcode',
    'https://creativecommons.org/licenses/by/3.0/us': 'https://creativecommons.org/licenses/by/3.0/legalcode',
    'https://creativecommons.org/licenses/by/4.0': 'https://creativecommons.org/licenses/by/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/1.0': 'https://creativecommons.org/licenses/by-nc/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/2.0': 'https://creativecommons.org/licenses/by-nc/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/2.5': 'https://creativecommons.org/licenses/by-nc/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nc/3.0': 'https://creativecommons.org/licenses/by-nc/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nc/4.0': 'https://creativecommons.org/licenses/by-nc/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/1.0': 'https://creativecommons.org/licenses/by-nd-nc/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/2.0': 'https://creativecommons.org/licenses/by-nd-nc/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/2.5': 'https://creativecommons.org/licenses/by-nd-nc/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/3.0': 'https://creativecommons.org/licenses/by-nd-nc/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nd-nc/4.0': 'https://creativecommons.org/licenses/by-nd-nc/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/1.0': 'https://creativecommons.org/licenses/by-nc-sa/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/2.0': 'https://creativecommons.org/licenses/by-nc-sa/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/2.5': 'https://creativecommons.org/licenses/by-nc-sa/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/3.0': 'https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-sa/4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/1.0': 'https://creativecommons.org/licenses/by-nd/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/2.0': 'https://creativecommons.org/licenses/by-nd/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/2.5': 'https://creativecommons.org/licenses/by-nd/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nd/3.0': 'https://creativecommons.org/licenses/by-nd/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nd/4.0': 'https://creativecommons.org/licenses/by-nd/2.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/1.0': 'https://creativecommons.org/licenses/by-sa/1.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/2.0': 'https://creativecommons.org/licenses/by-sa/2.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/2.5': 'https://creativecommons.org/licenses/by-sa/2.5/legalcode',
    'https://creativecommons.org/licenses/by-sa/3.0': 'https://creativecommons.org/licenses/by-sa/3.0/legalcode',
    'https://creativecommons.org/licenses/by-sa/4.0': 'https://creativecommons.org/licenses/by-sa/4.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/1.0': 'https://creativecommons.org/licenses/by-nc-nd/1.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/2.0': 'https://creativecommons.org/licenses/by-nc-nd/2.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/2.5': 'https://creativecommons.org/licenses/by-nc-nd/2.5/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/3.0': 'https://creativecommons.org/licenses/by-nc-nd/3.0/legalcode',
    'https://creativecommons.org/licenses/by-nc-nd/4.0': 'https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode',
    'https://creativecommons.org/licenses/publicdomain': 'https://creativecommons.org/licenses/publicdomain/',
    'https://creativecommons.org/publicdomain/zero/1.0': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode'
}

CR_TO_CP_TRANSLATIONS = {
    'Proceedings': None,
    'ReferenceBook': None,
    'JournalIssue': 'article-journal',
    'ProceedingsArticle': 'paper-conference',
    'Other': None,
    'Dissertation': 'thesis',
    'Dataset': 'dataset',
    'EditedBook': 'book',
    'PostedContent': 'article-journal',
    'JournalArticle': 'article-journal',
    'Journal': None,
    'Report': 'report',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': None,
    'BookSection': 'chapter',
    'BookPart': None,
    'Book': 'book',
    'BookChapter': 'chapter',
    'StandardSeries': None,
    'Monograph': 'book',
    'Component': None,
    'ReferenceEntry': 'entry-dictionary',
    'JournalVolume': None,
    'BookSet': None
}

CR_TO_SO_TRANSLATIONS = {
    'Proceedings': None,
    'ReferenceBook': 'Book',
    'JournalIssue': 'PublicationIssue',
    'ProceedingsArticle': None,
    'Other': 'CreativeWork',
    'Dissertation': 'Thesis',
    'Dataset': 'Dataset',
    'EditedBook': 'Book',
    'JournalArticle': 'ScholarlyArticle',
    'Journal': None,
    'Report': 'Report',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': None,
    'BookSection': None,
    'BookPart': None,
    'Book': 'Book',
    'BookChapter': 'Chapter',
    'StandardSeries': None,
    'Monograph': 'Book',
    'Component': 'CreativeWork',
    'ReferenceEntry': None,
    'JournalVolume': 'PublicationVolume',
    'BookSet': None,
    'PostedContent': 'ScholarlyArticle',
    'PeerReview': 'Review'
}

CR_TO_BIB_TRANSLATIONS = {
    'Proceedings': 'proceedings',
    'ReferenceBook': 'book',
    'JournalIssue': None,
    'ProceedingsArticle': None,
    'Other': None,
    'Dissertation': 'phdthesis',
    'Dataset': None,
    'EditedBook': 'book',
    'JournalArticle': 'article',
    'Journal': None,
    'Report': 'techreport',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': None,
    'BookSection': 'inbook',
    'BookPart': None,
    'Book': 'book',
    'BookChapter': 'inbook',
    'StandardSeries': None,
    'Monograph': 'book',
    'Component': None,
    'ReferenceEntry': None,
    'JournalVolume': None,
    'BookSet': None,
    'PostedContent': 'article'
}

CR_TO_RIS_TRANSLATIONS = {
    'Proceedings': 'CONF',
    'PostedContent': 'JOUR',
    'ReferenceBook': 'BOOK',
    'JournalIssue': 'JOUR',
    'ProceedingsArticle': 'CPAPER',
    'Other': 'GEN',
    'Dissertation': 'THES',
    'Dataset': 'DATA',
    'EditedBook': 'BOOK',
    'JournalArticle': 'JOUR',
    'Journal': None,
    'Report': 'RPRT',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': 'STAND',
    'BookSection': 'CHAP',
    'BookPart': 'CHAP',
    'Book': 'BOOK',
    'BookChapter': 'CHAP',
    'StandardSeries': None,
    'Monograph': 'BOOK',
    'Component': None,
    'ReferenceEntry': 'DICT',
    'JournalVolume': None,
    'BookSet': None
}

CR_TO_DC_TRANSLATIONS = {
    'Proceedings': None,
    'ReferenceBook': None,
    'JournalIssue': 'Text',
    'ProceedingsArticle': 'ConferencePaper',
    'Other': 'Other',
    'Dissertation': 'Dissertation',
    'Dataset': 'Dataset',
    'EditedBook': 'Book',
    'JournalArticle': 'JournalArticle',
    'Journal': 'Journal',
    'Report': 'Report',
    'BookSeries': None,
    'ReportSeries': None,
    'BookTrack': None,
    'Standard': 'Standard',
    'BookSection': 'BookChapter',
    'BookPart': None,
    'Book': 'Book',
    'BookChapter': 'BookChapter',
    'SaComponent': 'Text',
    'StandardSeries': 'Standard',
    'Monograph': 'Book',
    'Component': None,
    'ReferenceEntry': None,
    'JournalVolume': None,
    'BookSet': None,
    'PostedContent': 'Preprint',
    'PeerReview': 'PeerReview'
}

SO_TO_DC_RELATION_TYPES = {
    'citation': 'References',
    'isBasedOn': 'IsSupplementedBy',
    'sameAs': 'IsIdenticalTo',
    'isPartOf': 'IsPartOf',
    'hasPart': 'HasPart',
    'isPredecessor': 'IsPreviousVersionOf',
    'isSuccessor': 'IsNewVersionOf'
}

SO_TO_DC_REVERSE_RELATION_TYPES = {
    'citation': 'IsReferencedBy',
    'isBasedOn': 'IsSupplementTo',
    'sameAs': 'IsIdenticalTo',
    'isPartOf': 'HasPart',
    'hasPart': 'IsPartOf',
    'isPredecessor': 'IsNewVersionOf',
    'isSuccessor': 'IsPreviousVersionOf'
}

def get_date_from_date_parts(date_as_parts):
    """Get date from date parts"""
    if date_as_parts is None:
        return None
    date_parts = date_as_parts.get('date-parts', [])
    if len(date_parts) == 0:
        return None
    date_parts = date_parts[0]
    year = date_parts[0] if len(date_parts) > 0 else 0
    month = date_parts[1] if len(date_parts) > 1 else 0
    day = date_parts[2] if len(date_parts) > 2 else 0
    return get_date_from_parts(year, month, day)

def get_date_from_parts(year = 0, month = 0, day = 0):
    """Get date from parts"""
    arr = [str(year).rjust(4, '0'), str(month).rjust(2, '0'), str(day).rjust(2, '0')]
    arr = [e for i,e in enumerate(arr) if not (e == '00' or e == '0000')]
    return None if len(arr) == 0 else '-'.join(arr)

def wrap(item):
    """Turn None, dict, or list into list"""
    if item is None:
        return []
    if isinstance(item, list):
        return item
    return [item]

def unwrap(list):
    """Turn list into dict or None, depending on list size"""
    if len(list) == 0:
        return None
    if len(list) == 1:
        return list[0]
    return list

def presence(item):
    """Turn empty list, dict or str into None"""
    return None if len(item) == 0 else item

def compact(dict_or_list):
    """Remove None from dict or list"""
    if type(dict_or_list) in [None, str]:
        return dict_or_list
    if isinstance(dict_or_list, dict):
        return {k: v for k, v in dict_or_list.items() if v is not None}
    if isinstance(dict_or_list, list):
        arr = (list(map(lambda x: compact(x), dict_or_list)))
        return None if len(arr) == 0 else arr

def parse_attributes(element, **kwargs):
    """extract attributes from a string, dict or list"""
    content = kwargs.get('content', '__content__')

    if isinstance(element, str) and kwargs.get('content', None) is None:
        return html.unescape(element)
    if isinstance(element, dict):
        return element.get(html.unescape(content), None)
    if isinstance(element, list):
        arr = list(map(lambda x: x.get(html.unescape(content), None) 
            if isinstance(x, dict) else x, element))
        arr = arr[0] if kwargs.get('first') else unwrap(arr)
        return arr

def normalize_id(id, **kwargs):
    """Check for valid DOI or HTTP(S) URL"""
    if id is None:
        return None

    # check for valid DOI
    doi = normalize_doi(id, **kwargs)
    if doi is not None:
        return doi

    # check for valid HTTP uri
    uri = urlparse(id)
    return id if uri.netloc and uri.scheme in ['http', 'https'] else None

def crossref_api_url(doi):
    """Return the Crossref API URL for a given DOI"""
    return 'https://api.crossref.org/works/' + doi

def normalize_url(url):
    """Normalize URL"""
    if url is None:
        return None
    if url.endswith('/'):
        url = url.strip('/')
    if url.startswith('http://'):
        url = url.replace('http://', 'https://')
    return url

def normalize_cc_url(url):
    """Normalize Creative Commons URL"""
    if url is None:
        return None
    url = normalize_url(url)
    return NORMALIZED_LICENSES.get(url, url)

def normalize_orcid(orcid):
    """Normalize ORCID"""
    orcid = validate_orcid(orcid)
    if orcid is None:
        return None
    return 'https://orcid.org/' + orcid

def validate_orcid(orcid):
    """Validate ORCID"""
    m = re.search(r"\A(?:(?:http|https)://(?:(?:www|sandbox)?\.)?orcid\.org/)?(\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{3}[0-9X]+)\Z", orcid)
    if m is None:
        return None
    orcid = re.sub(' ', '-', m.group(1))
    return orcid

def dict_to_spdx(dict):
    """Convert a dict to SPDX"""
    file_path = os.path.join(os.path.dirname(__file__), 'resources/spdx/licenses.json')
    with open(file_path) as json_file:
        spdx = json.load(json_file).get('licenses')
    license = next((l for l in spdx if l['licenseId'].lower() == dict.get('rightsIdentifier', None) or l['seeAlso'][0]== dict.get('rightsURI', None)), None)
    if license is None:
        return dict
    #   license = spdx.find do |l|
    #     l['licenseId'].casecmp?(hsh['rightsIdentifier']) || l['seeAlso'].first == normalize_cc_url(hsh['rightsURI']) || l['name'] == hsh['rights'] || l['seeAlso'].first == normalize_cc_url(hsh['rights'])
    #   end
    return compact({
        'rights': license['name'],
        'rightsURI': license['seeAlso'][0],
        'rightsIdentifier': license['licenseId'].lower(),
        'rightsIdentifierScheme': 'SPDX',
        'schemeUri': 'https://spdx.org/licenses/',
        'lang': dict.get('lang', None)
    })


    #   else
    #     {
    #       'rights': hsh['__content__'] || hsh['rights'],
    #       'rightsUri': hsh['rightsURI'] || hsh['rightsUri'],
    #       'rightsIdentifier': hsh['rightsIdentifier'].present? ? hsh['rightsIdentifier'].downcase : nil,
    #       'rightsIdentifierScheme': hsh['rightsIdentifierScheme'],
    #       'schemeUri': hsh['schemeUri'],
    #       'lang': hsh['lang']
    #     }.compact
    #   end
    # end

def from_citeproc(element):
    """Convert a citeproc element to CSL"""
    el, formatted_element = {}, []
    for elem in wrap(element):
        if elem.get('literal', None) is not None:
            el['@type'] = 'Organization'
            el['name'] = el['literal']
        elif elem.get('name', None) is not None:
            el['@type'] = 'Organization'
        else:
            el['@type'] = 'Person'
            el['name'] = ' '.join(compact([elem.get('given', None), elem.get('family', None)]))
        el['givenName'] = elem.get('given', None)
        el['familyName'] = elem.get('family', None)
        el['affiliation'] = elem.get('affiliation', None)
        formatted_element.append(el)
    return formatted_element
