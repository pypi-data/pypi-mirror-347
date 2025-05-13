from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import _slidize

class ConverterOptions:
    '''Provides options that control how a presentation/slide is rendered.'''
    def __init__(self):
        ...

    @property
    def slides_view_options(self) -> SlidesViewOptions:
        ...

    @slides_view_options.setter
    def slides_view_options(self, value: SlidesViewOptions):
        ...

    @property
    def default_regular_font(self) -> str:
        ...

    @default_regular_font.setter
    def default_regular_font(self, value: str):
        ...

    ...

class HandoutViewOptions:
    '''Represents the handout presentation view mode for export.'''
    def __init__(self):
        ...

    @property
    def handout(self) -> HandoutViewType:
        ...

    @handout.setter
    def handout(self, value: HandoutViewType):
        ...

    @property
    def print_slide_numbers(self) -> bool:
        ...

    @print_slide_numbers.setter
    def print_slide_numbers(self, value: bool):
        ...

    @property
    def print_frame_slide(self) -> bool:
        ...

    @print_frame_slide.setter
    def print_frame_slide(self, value: bool):
        ...

    @property
    def print_comments(self) -> bool:
        ...

    @print_comments.setter
    def print_comments(self, value: bool):
        ...

    ...

class HtmlConverterOptions:
    '''Provides options that control how a presentation is converted to HTML format.'''
    def __init__(self):
        ...

    @property
    def slides_view_options(self) -> SlidesViewOptions:
        ...

    @slides_view_options.setter
    def slides_view_options(self, value: SlidesViewOptions):
        ...

    @property
    def default_regular_font(self) -> str:
        ...

    @default_regular_font.setter
    def default_regular_font(self, value: str):
        ...

    @property
    def show_hidden_slides(self) -> bool:
        ...

    @show_hidden_slides.setter
    def show_hidden_slides(self, value: bool):
        ...

    @property
    def save_slide_in_svg_format(self) -> bool:
        ...

    @save_slide_in_svg_format.setter
    def save_slide_in_svg_format(self, value: bool):
        ...

    @property
    def slide_image_scale(self) -> float:
        ...

    @slide_image_scale.setter
    def slide_image_scale(self, value: float):
        ...

    @property
    def jpeg_quality(self) -> int:
        ...

    @jpeg_quality.setter
    def jpeg_quality(self, value: int):
        ...

    @property
    def pictures_compression(self) -> PicturesCompressionLevel:
        ...

    @pictures_compression.setter
    def pictures_compression(self, value: PicturesCompressionLevel):
        ...

    @property
    def delete_pictures_cropped_areas(self) -> bool:
        ...

    @delete_pictures_cropped_areas.setter
    def delete_pictures_cropped_areas(self, value: bool):
        ...

    ...

class ImageConverterOptions:
    '''Provides options that control how a presentation slides should be rendered.'''
    def __init__(self):
        ...

    @property
    def slides_view_options(self) -> SlidesViewOptions:
        ...

    @slides_view_options.setter
    def slides_view_options(self, value: SlidesViewOptions):
        ...

    @property
    def default_regular_font(self) -> str:
        ...

    @default_regular_font.setter
    def default_regular_font(self, value: str):
        ...

    @property
    def image_width(self) -> int:
        ...

    @image_width.setter
    def image_width(self, value: int):
        ...

    @property
    def image_height(self) -> int:
        ...

    @image_height.setter
    def image_height(self, value: int):
        ...

    @property
    def image_scale(self) -> float:
        ...

    @image_scale.setter
    def image_scale(self, value: float):
        ...

    ...

class License:
    '''Provides methods for license management.'''
    @overload
    @staticmethod
    def plug_license(path: str) -> None:
        ...

    @overload
    @staticmethod
    def plug_license(stream: io.RawIOBase) -> None:
        ...

    ...

class NotesCommentsViewOptions:
    '''Provides options that control the view of notes and comments in exported document.'''
    def __init__(self):
        ...

    @property
    def notes_position(self) -> NotesPositions:
        ...

    @notes_position.setter
    def notes_position(self, value: NotesPositions):
        ...

    @property
    def comments_position(self) -> CommentsPositions:
        ...

    @comments_position.setter
    def comments_position(self, value: CommentsPositions):
        ...

    @property
    def comments_area_color(self) -> aspose.pydrawing.Color:
        ...

    @comments_area_color.setter
    def comments_area_color(self, value: aspose.pydrawing.Color):
        ...

    @property
    def comments_area_width(self) -> int:
        ...

    @comments_area_width.setter
    def comments_area_width(self, value: int):
        ...

    @property
    def show_comments_by_no_author(self) -> bool:
        ...

    @show_comments_by_no_author.setter
    def show_comments_by_no_author(self, value: bool):
        ...

    ...

class PdfConverterOptions:
    '''Provides options that control how a presentation is converted to PDF format.'''
    def __init__(self):
        ...

    @property
    def slides_view_options(self) -> SlidesViewOptions:
        ...

    @slides_view_options.setter
    def slides_view_options(self, value: SlidesViewOptions):
        ...

    @property
    def default_regular_font(self) -> str:
        ...

    @default_regular_font.setter
    def default_regular_font(self, value: str):
        ...

    @property
    def show_hidden_slides(self) -> bool:
        ...

    @show_hidden_slides.setter
    def show_hidden_slides(self, value: bool):
        ...

    @property
    def compliance_level(self) -> PdfComplianceLevel:
        ...

    @compliance_level.setter
    def compliance_level(self, value: PdfComplianceLevel):
        ...

    @property
    def use_flat_text_compression(self) -> bool:
        ...

    @use_flat_text_compression.setter
    def use_flat_text_compression(self, value: bool):
        ...

    @property
    def embed_true_type_fonts_for_ascii(self) -> bool:
        ...

    @embed_true_type_fonts_for_ascii.setter
    def embed_true_type_fonts_for_ascii(self, value: bool):
        ...

    @property
    def embed_full_fonts(self) -> bool:
        ...

    @embed_full_fonts.setter
    def embed_full_fonts(self, value: bool):
        ...

    @property
    def rasterize_unsupported_font_styles(self) -> bool:
        ...

    @rasterize_unsupported_font_styles.setter
    def rasterize_unsupported_font_styles(self, value: bool):
        ...

    @property
    def best_images_compression_ratio(self) -> bool:
        ...

    @best_images_compression_ratio.setter
    def best_images_compression_ratio(self, value: bool):
        ...

    @property
    def jpeg_quality(self) -> int:
        ...

    @jpeg_quality.setter
    def jpeg_quality(self, value: int):
        ...

    @property
    def save_metafiles_as_png(self) -> bool:
        ...

    @save_metafiles_as_png.setter
    def save_metafiles_as_png(self, value: bool):
        ...

    @property
    def sufficient_resolution(self) -> float:
        ...

    @sufficient_resolution.setter
    def sufficient_resolution(self, value: float):
        ...

    @property
    def password(self) -> str:
        ...

    @password.setter
    def password(self, value: str):
        ...

    @property
    def include_ole_data(self) -> bool:
        ...

    @include_ole_data.setter
    def include_ole_data(self, value: bool):
        ...

    ...

class PresentationConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into various presentation formats.'''
    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, convert_format: ConvertFormat) -> None:
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase, convert_format: ConvertFormat) -> None:
        ...

    ...

class PresentationMerger:
    '''Plugin for merging PowerPoint files of the same format into one file.'''
    @staticmethod
    def process(input_file_names: List[str], output_file_name: str) -> None:
        ...

    ...

class PresentationTextExtractor:
    '''Plugin for extracting text from the PowerPoint 97-2003 and Microsoft Office Open XML presentations.'''
    @overload
    @staticmethod
    def process(input_file_name: str, text_extraction_mode: TextExtractionMode) -> List[SlideText]:
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, text_extraction_mode: TextExtractionMode) -> List[SlideText]:
        ...

    ...

class PresentationToHtmlConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into HTML format.'''
    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: HtmlConverterOptions) -> None:
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase) -> None:
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase, options: HtmlConverterOptions) -> None:
        ...

    ...

class PresentationToJpegConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of JPEG images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: ImageConverterOptions) -> None:
        ...

    ...

class PresentationToPdfConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into PDF format.'''
    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: PdfConverterOptions) -> None:
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase) -> None:
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase, options: PdfConverterOptions) -> None:
        ...

    ...

class PresentationToPngConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of PNG images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: ImageConverterOptions) -> None:
        ...

    ...

class PresentationToSvgConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of SVG format images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: SvgConverterOptions) -> None:
        ...

    ...

class PresentationToTiffConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of TIFF images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: TiffConverterOptions) -> None:
        ...

    ...

class SlideText:
    '''Represents the text extracted from the presentation slide.'''
    @property
    def text(self) -> str:
        ...

    @property
    def master_text(self) -> str:
        ...

    @property
    def layout_text(self) -> str:
        ...

    @property
    def notes_text(self) -> str:
        ...

    @property
    def comments_text(self) -> str:
        ...

    ...

class SlidesViewOptions:
    '''Represents the presentation view mode for export.'''
    ...

class SvgConverterOptions:
    '''Provides options that control how a presentation is converted to SVG format.'''
    def __init__(self):
        ...

    @property
    def default_regular_font(self) -> str:
        ...

    @default_regular_font.setter
    def default_regular_font(self, value: str):
        ...

    @property
    def use_frame_size(self) -> bool:
        ...

    @use_frame_size.setter
    def use_frame_size(self, value: bool):
        ...

    @property
    def use_frame_rotation(self) -> bool:
        ...

    @use_frame_rotation.setter
    def use_frame_rotation(self, value: bool):
        ...

    @property
    def vectorize_text(self) -> bool:
        ...

    @vectorize_text.setter
    def vectorize_text(self, value: bool):
        ...

    @property
    def metafile_rasterization_dpi(self) -> int:
        ...

    @metafile_rasterization_dpi.setter
    def metafile_rasterization_dpi(self, value: int):
        ...

    @property
    def jpeg_quality(self) -> int:
        ...

    @jpeg_quality.setter
    def jpeg_quality(self, value: int):
        ...

    @property
    def pictures_compression(self) -> PicturesCompressionLevel:
        ...

    @pictures_compression.setter
    def pictures_compression(self, value: PicturesCompressionLevel):
        ...

    @property
    def delete_pictures_cropped_areas(self) -> bool:
        ...

    @delete_pictures_cropped_areas.setter
    def delete_pictures_cropped_areas(self, value: bool):
        ...

    @property
    def link_external_fonts(self) -> bool:
        ...

    @link_external_fonts.setter
    def link_external_fonts(self, value: bool):
        ...

    ...

class TiffConverterOptions:
    '''Provides options that control how a presentation is converted to TIFF format.'''
    def __init__(self):
        ...

    @property
    def slides_view_options(self) -> SlidesViewOptions:
        ...

    @slides_view_options.setter
    def slides_view_options(self, value: SlidesViewOptions):
        ...

    @property
    def default_regular_font(self) -> str:
        ...

    @default_regular_font.setter
    def default_regular_font(self, value: str):
        ...

    @property
    def show_hidden_slides(self) -> bool:
        ...

    @show_hidden_slides.setter
    def show_hidden_slides(self, value: bool):
        ...

    @property
    def multi_page(self) -> bool:
        ...

    @multi_page.setter
    def multi_page(self, value: bool):
        ...

    @property
    def image_width(self) -> int:
        ...

    @image_width.setter
    def image_width(self, value: int):
        ...

    @property
    def image_height(self) -> int:
        ...

    @image_height.setter
    def image_height(self, value: int):
        ...

    @property
    def dpi(self) -> int:
        ...

    @dpi.setter
    def dpi(self, value: int):
        ...

    @property
    def compression_type(self) -> TiffCompressionTypes:
        ...

    @compression_type.setter
    def compression_type(self, value: TiffCompressionTypes):
        ...

    @property
    def pixel_format(self) -> ImagePixelFormat:
        ...

    @pixel_format.setter
    def pixel_format(self, value: ImagePixelFormat):
        ...

    @property
    def black_white_mode(self) -> BlackWhiteConversionMode:
        ...

    @black_white_mode.setter
    def black_white_mode(self, value: BlackWhiteConversionMode):
        ...

    ...

class BlackWhiteConversionMode:
    '''Provides options that control how slides' images will be converted to bitonal images.'''
    @classmethod
    @property
    def DEFAULT(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def DITHERING(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def DITHERING_FLOYD_STEINBERG(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def AUTO(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def AUTO_OTSU(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def THRESHOLD25(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def THRESHOLD50(cls) -> BlackWhiteConversionMode:
        ...

    @classmethod
    @property
    def THRESHOLD75(cls) -> BlackWhiteConversionMode:
        ...

    ...

class CommentsPositions:
    '''Represents the rule to render comments into exported document'''
    @classmethod
    @property
    def NONE(cls) -> CommentsPositions:
        ...

    @classmethod
    @property
    def BOTTOM(cls) -> CommentsPositions:
        ...

    @classmethod
    @property
    def RIGHT(cls) -> CommentsPositions:
        ...

    ...

class ConvertFormat:
    '''Specifies the format of a converted presentation.'''
    @classmethod
    @property
    def PPT(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def PPTX(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def PPTM(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def PPS(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def PPSX(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def PPSM(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def POT(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def POTX(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def POTM(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def ODP(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def OTP(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def FODP(cls) -> ConvertFormat:
        ...

    @classmethod
    @property
    def XML(cls) -> ConvertFormat:
        ...

    ...

class HandoutViewType:
    '''Specifies how many slides and in what sequence will be placed on the page.'''
    @classmethod
    @property
    def HANDOUTS1(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS2(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS3(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS_4_HORIZONTAL(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS_4_VERTICAL(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS_6_HORIZONTAL(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS_6_VERTICAL(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS_9_HORIZONTAL(cls) -> HandoutViewType:
        ...

    @classmethod
    @property
    def HANDOUTS_9_VERTICAL(cls) -> HandoutViewType:
        ...

    ...

class ImagePixelFormat:
    '''Specifies the pixel format for the generated images.'''
    @classmethod
    @property
    def FORMAT_1BPP_INDEXED(cls) -> ImagePixelFormat:
        ...

    @classmethod
    @property
    def FORMAT_4BPP_INDEXED(cls) -> ImagePixelFormat:
        ...

    @classmethod
    @property
    def FORMAT_8BPP_INDEXED(cls) -> ImagePixelFormat:
        ...

    @classmethod
    @property
    def FORMAT_24BPP_RGB(cls) -> ImagePixelFormat:
        ...

    @classmethod
    @property
    def FORMAT_32BPP_ARGB(cls) -> ImagePixelFormat:
        ...

    ...

class NotesPositions:
    '''Represents the rule to render notes into exported document'''
    @classmethod
    @property
    def NONE(cls) -> NotesPositions:
        ...

    @classmethod
    @property
    def BOTTOM_FULL(cls) -> NotesPositions:
        ...

    @classmethod
    @property
    def BOTTOM_TRUNCATED(cls) -> NotesPositions:
        ...

    ...

class PdfComplianceLevel:
    '''Constants which define the PDF standards compliance level.'''
    @classmethod
    @property
    def PDF15(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF16(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF17(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A1B(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A1A(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A2B(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A2A(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A3B(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A3A(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_UA(cls) -> PdfComplianceLevel:
        ...

    @classmethod
    @property
    def PDF_A2U(cls) -> PdfComplianceLevel:
        ...

    ...

class PicturesCompressionLevel:
    '''Represents the pictures compression level'''
    @classmethod
    @property
    def DPI330(cls) -> PicturesCompressionLevel:
        ...

    @classmethod
    @property
    def DPI220(cls) -> PicturesCompressionLevel:
        ...

    @classmethod
    @property
    def DPI150(cls) -> PicturesCompressionLevel:
        ...

    @classmethod
    @property
    def DPI96(cls) -> PicturesCompressionLevel:
        ...

    @classmethod
    @property
    def DPI72(cls) -> PicturesCompressionLevel:
        ...

    @classmethod
    @property
    def DOCUMENT_RESOLUTION(cls) -> PicturesCompressionLevel:
        ...

    ...

class TextExtractionMode:
    '''Specifies the text extraction mode.'''
    @classmethod
    @property
    def UNARRANGED(cls) -> TextExtractionMode:
        ...

    @classmethod
    @property
    def ARRANGED(cls) -> TextExtractionMode:
        ...

    ...

class TiffCompressionTypes:
    '''Provides options that control how a presentation is compressed in TIFF format.'''
    @classmethod
    @property
    def DEFAULT(cls) -> TiffCompressionTypes:
        ...

    @classmethod
    @property
    def NONE(cls) -> TiffCompressionTypes:
        ...

    @classmethod
    @property
    def CCITT3(cls) -> TiffCompressionTypes:
        ...

    @classmethod
    @property
    def CCITT4(cls) -> TiffCompressionTypes:
        ...

    @classmethod
    @property
    def LZW(cls) -> TiffCompressionTypes:
        ...

    @classmethod
    @property
    def RLE(cls) -> TiffCompressionTypes:
        ...

    ...

