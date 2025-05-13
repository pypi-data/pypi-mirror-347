from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import slidize

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

class HandoutViewOptions(SlidesViewOptions):
    '''Represents the handout presentation view mode for export.'''
    def __init__(self):
        '''Initializes a new instance of the HandoutViewOptions class.'''
        ...

    @property
    def handout(self) -> HandoutViewType:
        '''Specifies how many slides and in what sequence will be placed on the page :py:enum:`slidize.HandoutViewType`.'''
        ...

    @handout.setter
    def handout(self, value: HandoutViewType):
        '''Specifies how many slides and in what sequence will be placed on the page :py:enum:`slidize.HandoutViewType`.'''
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

class HtmlConverterOptions(ConverterOptions):
    '''Provides options that control how a presentation is converted to HTML format.'''
    def __init__(self):
        '''Initializes a new instance of the HtmlConverterOptions class.'''
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

class ImageConverterOptions(ConverterOptions):
    '''Provides options that control how a presentation slides should be rendered.'''
    def __init__(self):
        '''Initializes a new instance of the ImageConverterOptions class.'''
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
        '''Plugs license from the specified file path.
        :param path: The path to the license file.'''
        ...

    @overload
    @staticmethod
    def plug_license(stream: io.RawIOBase) -> None:
        '''Plugs license from the specified stream.
        :param stream: The stream from which to read the license data.'''
        ...

    ...

class NotesCommentsViewOptions(SlidesViewOptions):
    '''Provides options that control the view of notes and comments in exported document.'''
    def __init__(self):
        '''Initializes a new instance of the NotesCommentsViewOptions class.'''
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

class PdfConverterOptions(ConverterOptions):
    '''Provides options that control how a presentation is converted to PDF format.'''
    def __init__(self):
        '''Initializes a new instance of the PdfConverterOptions class.'''
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
        '''Setting user password to protect the PDF document. 
                    Read/write :py:class:`str`.'''
        ...

    @password.setter
    def password(self, value: str):
        '''Setting user password to protect the PDF document. 
                    Read/write :py:class:`str`.'''
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
        '''Converts the input presentation using the output file extension to determine the required convert format.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The name of the output presentation file.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, convert_format: ConvertFormat) -> None:
        '''Converts the input presentation to a file with the specified format.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The name of the output presentation file.
        :param convert_format: The format to which the presentation should be converted.'''
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase, convert_format: ConvertFormat) -> None:
        '''Converts the input presentation to the specified format.
        :param input_stream: The input presentation stream.
        :param output_stream: The output stream.
        :param convert_format: The format to which the presentation should be converted.'''
        ...

    ...

class PresentationMerger:
    '''Plugin for merging PowerPoint files of the same format into one file.'''
    @staticmethod
    def process(input_file_names: List[str], output_file_name: str) -> None:
        '''Merges the PowerPoint files from the array into one file.
        :param input_file_names: Array of the input presentation file names.
        :param output_file_name: The output file name.'''
        ...

    ...

class PresentationTextExtractor:
    '''Plugin for extracting text from the PowerPoint 97-2003 and Microsoft Office Open XML presentations.'''
    @overload
    @staticmethod
    def process(input_file_name: str, text_extraction_mode: TextExtractionMode) -> List[SlideText]:
        '''Extracts text from the input presentation using the specified mode.
        :param input_file_name: The name of the input presentation file.
        :param text_extraction_mode: The text extraction mode.'''
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, text_extraction_mode: TextExtractionMode) -> List[SlideText]:
        '''Extracts text from the input presentation using the specified mode.
        :param input_stream: The input presentation stream.
        :param text_extraction_mode: The text extraction mode.'''
        ...

    ...

class PresentationToHtmlConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into HTML format.'''
    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        '''Converts the input presentation to HTML format.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: HtmlConverterOptions) -> None:
        '''Converts the input presentation to HTML format with custom options.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.
        :param options: HTML converter options.'''
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase) -> None:
        '''Converts the input presentation to HTML format.
        :param input_stream: The input presentation stream.
        :param output_stream: The output stream.'''
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase, options: HtmlConverterOptions) -> None:
        '''Converts the input presentation to HTML format with custom options.
        :param input_stream: The input presentation stream.
        :param output_stream: The output stream.
        :param options: HTML converter options.'''
        ...

    ...

class PresentationToJpegConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of JPEG images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        '''Converts the input presentation to a set of JPEG format images and saves them in the folder of the input presentation. 
                    If the input file name is given as "myPath/myFilename.pptx", 
                    the result will be saved as a set of "myPath/myFilename_N.jpeg" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        '''Converts the input presentation to a set of JPEG format images.  
                    If the output file name is given as "myPath/myFilename.jpeg", 
                    the result will be saved as a set of "myPath/myFilename_N.jpeg" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: ImageConverterOptions) -> None:
        '''Converts the input presentation to a set of PNG format images with custom options. 
                    If the output file name is given as "myPath/myFilename.jpeg", 
                    the result will be saved as a set of "myPath/myFilename_N.jpeg" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.
        :param options: Image converter options.'''
        ...

    ...

class PresentationToPdfConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into PDF format.'''
    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        '''Converts the input presentation to PDF format.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: PdfConverterOptions) -> None:
        '''Converts the input presentation to PDF format with custom options.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.
        :param options: PDF converter options.'''
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase) -> None:
        '''Converts the input presentation to PDF format.
        :param input_stream: The input presentation stream.
        :param output_stream: The output stream.'''
        ...

    @overload
    @staticmethod
    def process(input_stream: io.RawIOBase, output_stream: io.RawIOBase, options: PdfConverterOptions) -> None:
        '''Converts the input presentation to PDF format with custom options.
        :param input_stream: The input presentation stream.
        :param output_stream: The output stream.
        :param options: PDF converter options.'''
        ...

    ...

class PresentationToPngConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of PNG images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        '''Converts the input presentation to a set of PNG format images and saves them in the folder of the input presentation.  
                    If the input file name is given as "myPath/myFilename.pptx", 
                    the result will be saved as a set of "myPath/myFilename_N.png" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        '''Converts the input presentation to a set of PNG format images. 
                    If the output file name is given as "myPath/myFilename.png", 
                    the result will be saved as a set of "myPath/myFilename_N.png" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: ImageConverterOptions) -> None:
        '''Converts the input presentation to a set of PNG format images with custom options. 
                    If the output file name is given as "myPath/myFilename.png", 
                    the result will be saved as a set of "myPath/myFilename_N.png" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.
        :param options: Image converter options.'''
        ...

    ...

class PresentationToSvgConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of SVG format images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        '''Converts the input presentation to a set of SVG format images and saves them in the folder of the input presentation. 
                    If the input file name is given as "myPath/myFilename.pptx", 
                    the result will be saved as a set of "myPath/myFilename_N.svg" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        '''Converts the input presentation to a set of SVG format images.  
                    If the output file name is given as "myPath/myFilename.svg", 
                    the result will be saved as a set of "myPath/myFilename_N.svg" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: SvgConverterOptions) -> None:
        '''Converts the input presentation to a set of SVG format images with custom options.
                    If the output file name is given as "myPath/myFilename.svg", 
                    the result will be saved as a set of "myPath/myFilename_N.svg" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.
        :param options: SVG converter options.'''
        ...

    ...

class PresentationToTiffConverter:
    '''Plugin for converting the PowerPoint 97-2003 and Microsoft Office Open XML presentations into a set of TIFF images.'''
    @overload
    @staticmethod
    def process(input_file_name: str) -> None:
        '''Converts the input presentation to a set of TIFF format images and saves them in the folder of the input presentation.  
                    If the input file name is given as "myPath/myFilename.pptx", 
                    the result will be saved as a set of "myPath/myFilename_N.tiff" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str) -> None:
        '''Converts the input presentation to a set of TIFF images. 
                    If the output file name is given as "myPath/myFilename.tiff", 
                    the result will be saved as a set of "myPath/myFilename_N.tiff" files, where N is a slide number.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.'''
        ...

    @overload
    @staticmethod
    def process(input_file_name: str, output_file_name: str, options: TiffConverterOptions) -> None:
        '''Converts the input presentation to TIFF format with custom options.
                    If the output file name is given as "myPath/myFilename.tiff" and :py:attr:`slidize.TiffConverterOptions.multi_page` is ``false``, 
                    the result will be saved as a set of "myPath/myFilename_N.tiff" files, where N is a slide number.
                    Otherwise, if :py:attr:`slidize.TiffConverterOptions.multi_page` is ``true``, the result will be a multi-page "myPath/myFilename.tiff" document.
        :param input_file_name: The name of the input presentation file.
        :param output_file_name: The output file name.
        :param options: TIFF converter options.'''
        ...

    ...

class SlideText:
    '''Represents the text extracted from the presentation slide.'''
    @property
    def text(self) -> str:
        '''The text from the slide shapes.'''
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
        '''Initializes a new instance of the SvgConverterOptions class.'''
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

class TiffConverterOptions(ConverterOptions):
    '''Provides options that control how a presentation is converted to TIFF format.'''
    def __init__(self):
        '''Initializes a new instance of the TiffConverterOptions class.'''
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
        '''Returns or sets the resolution of the generated TIFF image.
                    Read/write :py:class:`int`.'''
        ...

    @dpi.setter
    def dpi(self, value: int):
        '''Returns or sets the resolution of the generated TIFF image.
                    Read/write :py:class:`int`.'''
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
        '''Specifies no conversion algorithm. The algorithm implemented in the TIFF codec will be used. (Default)'''
        ...

    @classmethod
    @property
    def DITHERING(cls) -> BlackWhiteConversionMode:
        '''Specifies the dithering algorithm (Floyd-Steinberg).'''
        ...

    @classmethod
    @property
    def DITHERING_FLOYD_STEINBERG(cls) -> BlackWhiteConversionMode:
        '''Specifies the Floyd-Steinberg dithering algorithm.'''
        ...

    @classmethod
    @property
    def AUTO(cls) -> BlackWhiteConversionMode:
        '''Specifies the automatically calculated threshold algorithm (Otsu).'''
        ...

    @classmethod
    @property
    def AUTO_OTSU(cls) -> BlackWhiteConversionMode:
        '''Specifies the automatically calculated Otsu's threshold algorithm.'''
        ...

    @classmethod
    @property
    def THRESHOLD25(cls) -> BlackWhiteConversionMode:
        '''Specifies the static threshold algorithm (25%).'''
        ...

    @classmethod
    @property
    def THRESHOLD50(cls) -> BlackWhiteConversionMode:
        '''Specifies the static threshold algorithm (50%).'''
        ...

    @classmethod
    @property
    def THRESHOLD75(cls) -> BlackWhiteConversionMode:
        '''Specifies the static threshold algorithm (75%).'''
        ...

    ...

class CommentsPositions:
    '''Represents the rule to render comments into exported document'''
    @classmethod
    @property
    def NONE(cls) -> CommentsPositions:
        '''Specifies that comments should not be displayed at all.'''
        ...

    @classmethod
    @property
    def BOTTOM(cls) -> CommentsPositions:
        '''Specifies that comments should be displayed at the bottom of the page.'''
        ...

    @classmethod
    @property
    def RIGHT(cls) -> CommentsPositions:
        '''Specifies that comments should be displayed to the right of the page.'''
        ...

    ...

class ConvertFormat:
    '''Specifies the format of a converted presentation.'''
    @classmethod
    @property
    def PPT(cls) -> ConvertFormat:
        '''Convert presentation to PPT format.'''
        ...

    @classmethod
    @property
    def PPTX(cls) -> ConvertFormat:
        '''Convert presentation to PPTX format.'''
        ...

    @classmethod
    @property
    def PPTM(cls) -> ConvertFormat:
        '''Convert presentation to PPTM (macro-enabled presentation) format.'''
        ...

    @classmethod
    @property
    def PPS(cls) -> ConvertFormat:
        '''Convert presentation to PPS format.'''
        ...

    @classmethod
    @property
    def PPSX(cls) -> ConvertFormat:
        '''Convert presentation to PPSX (slideshow) format.'''
        ...

    @classmethod
    @property
    def PPSM(cls) -> ConvertFormat:
        '''Convert presentation to PPSM (macro-enabled slideshow) format.'''
        ...

    @classmethod
    @property
    def POT(cls) -> ConvertFormat:
        '''Convert presentation to POT format.'''
        ...

    @classmethod
    @property
    def POTX(cls) -> ConvertFormat:
        '''Convert presentation to POTX (template) format.'''
        ...

    @classmethod
    @property
    def POTM(cls) -> ConvertFormat:
        '''Convert presentation to POTM (macro-enabled template) format.'''
        ...

    @classmethod
    @property
    def ODP(cls) -> ConvertFormat:
        '''Convert presentation to ODP format.'''
        ...

    @classmethod
    @property
    def OTP(cls) -> ConvertFormat:
        '''Convert presentation to OTP (presentation template) format.'''
        ...

    @classmethod
    @property
    def FODP(cls) -> ConvertFormat:
        '''Convert presentation to FODP format.'''
        ...

    @classmethod
    @property
    def XML(cls) -> ConvertFormat:
        '''Convert presentation to PowerPoint XML Presentation format.'''
        ...

    ...

class HandoutViewType:
    '''Specifies how many slides and in what sequence will be placed on the page.'''
    @classmethod
    @property
    def HANDOUTS1(cls) -> HandoutViewType:
        '''One slide per page.'''
        ...

    @classmethod
    @property
    def HANDOUTS2(cls) -> HandoutViewType:
        '''Two slides per page.'''
        ...

    @classmethod
    @property
    def HANDOUTS3(cls) -> HandoutViewType:
        '''Three slides per page.'''
        ...

    @classmethod
    @property
    def HANDOUTS_4_HORIZONTAL(cls) -> HandoutViewType:
        '''Four slides per page in a horizontal sequence.'''
        ...

    @classmethod
    @property
    def HANDOUTS_4_VERTICAL(cls) -> HandoutViewType:
        '''Four slides per page in a vertical sequence.'''
        ...

    @classmethod
    @property
    def HANDOUTS_6_HORIZONTAL(cls) -> HandoutViewType:
        '''Six slides per page in a horizontal sequence.'''
        ...

    @classmethod
    @property
    def HANDOUTS_6_VERTICAL(cls) -> HandoutViewType:
        '''Six slides per page in a vertical sequence.'''
        ...

    @classmethod
    @property
    def HANDOUTS_9_HORIZONTAL(cls) -> HandoutViewType:
        '''Nine slides per page in a horizontal sequence.'''
        ...

    @classmethod
    @property
    def HANDOUTS_9_VERTICAL(cls) -> HandoutViewType:
        '''Nine slides per page in a vertical sequence.'''
        ...

    ...

class ImagePixelFormat:
    '''Specifies the pixel format for the generated images.'''
    @classmethod
    @property
    def FORMAT_1BPP_INDEXED(cls) -> ImagePixelFormat:
        '''1 bits per pixel, indexed.'''
        ...

    @classmethod
    @property
    def FORMAT_4BPP_INDEXED(cls) -> ImagePixelFormat:
        '''4 bits per pixel, indexed.'''
        ...

    @classmethod
    @property
    def FORMAT_8BPP_INDEXED(cls) -> ImagePixelFormat:
        '''8 bits per pixel, indexed.'''
        ...

    @classmethod
    @property
    def FORMAT_24BPP_RGB(cls) -> ImagePixelFormat:
        '''24 bits per pixel, RGB.'''
        ...

    @classmethod
    @property
    def FORMAT_32BPP_ARGB(cls) -> ImagePixelFormat:
        '''32 bits per pixel, ARGB.'''
        ...

    ...

class NotesPositions:
    '''Represents the rule to render notes into exported document'''
    @classmethod
    @property
    def NONE(cls) -> NotesPositions:
        '''Specifies that notes should not be displayed at all.'''
        ...

    @classmethod
    @property
    def BOTTOM_FULL(cls) -> NotesPositions:
        '''Specifies that notes should be full displayed using additional pages as it is needed.'''
        ...

    @classmethod
    @property
    def BOTTOM_TRUNCATED(cls) -> NotesPositions:
        '''Specifies that notes should be displayed in only one page.'''
        ...

    ...

class PdfComplianceLevel:
    '''Constants which define the PDF standards compliance level.'''
    @classmethod
    @property
    def PDF15(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF 1.5 standard.'''
        ...

    @classmethod
    @property
    def PDF16(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF 1.6 standard.'''
        ...

    @classmethod
    @property
    def PDF17(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF 1.7 standard.'''
        ...

    @classmethod
    @property
    def PDF_A1B(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-1b standard.'''
        ...

    @classmethod
    @property
    def PDF_A1A(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-1a standard.'''
        ...

    @classmethod
    @property
    def PDF_A2B(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-2b standard.'''
        ...

    @classmethod
    @property
    def PDF_A2A(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-2a standard.'''
        ...

    @classmethod
    @property
    def PDF_A3B(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-3b standard.'''
        ...

    @classmethod
    @property
    def PDF_A3A(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-3a standard.'''
        ...

    @classmethod
    @property
    def PDF_UA(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/UA standard.'''
        ...

    @classmethod
    @property
    def PDF_A2U(cls) -> PdfComplianceLevel:
        '''The output file will comply with the PDF/A-2u standard.'''
        ...

    ...

class PicturesCompressionLevel:
    '''Represents the pictures compression level'''
    @classmethod
    @property
    def DPI330(cls) -> PicturesCompressionLevel:
        '''Good quality for high-definition (HD) displays'''
        ...

    @classmethod
    @property
    def DPI220(cls) -> PicturesCompressionLevel:
        '''Excellent quality on most printers and screens'''
        ...

    @classmethod
    @property
    def DPI150(cls) -> PicturesCompressionLevel:
        '''Good for web pages and projectors'''
        ...

    @classmethod
    @property
    def DPI96(cls) -> PicturesCompressionLevel:
        '''Minimize document size for sharing'''
        ...

    @classmethod
    @property
    def DPI72(cls) -> PicturesCompressionLevel:
        '''Default compression level'''
        ...

    @classmethod
    @property
    def DOCUMENT_RESOLUTION(cls) -> PicturesCompressionLevel:
        '''Use document resolution - the picture will not be compressed and used in document as-is'''
        ...

    ...

class TextExtractionMode:
    '''Specifies the text extraction mode.'''
    @classmethod
    @property
    def UNARRANGED(cls) -> TextExtractionMode:
        '''Extracts the raw text with no respect to position on the presentation slide.'''
        ...

    @classmethod
    @property
    def ARRANGED(cls) -> TextExtractionMode:
        '''Extracts text with position in the same order as on the presentation slide.'''
        ...

    ...

class TiffCompressionTypes:
    '''Provides options that control how a presentation is compressed in TIFF format.'''
    @classmethod
    @property
    def DEFAULT(cls) -> TiffCompressionTypes:
        '''Specifies the default compression scheme (LZW).'''
        ...

    @classmethod
    @property
    def NONE(cls) -> TiffCompressionTypes:
        '''Specifies no compression.'''
        ...

    @classmethod
    @property
    def CCITT3(cls) -> TiffCompressionTypes:
        '''Specifies the CCITT3 compression scheme.'''
        ...

    @classmethod
    @property
    def CCITT4(cls) -> TiffCompressionTypes:
        '''Specifies the CCITT4 compression scheme.'''
        ...

    @classmethod
    @property
    def LZW(cls) -> TiffCompressionTypes:
        '''Specifies the LZW compression scheme (Default).'''
        ...

    @classmethod
    @property
    def RLE(cls) -> TiffCompressionTypes:
        '''Specifies the RLE compression scheme.'''
        ...

    ...

